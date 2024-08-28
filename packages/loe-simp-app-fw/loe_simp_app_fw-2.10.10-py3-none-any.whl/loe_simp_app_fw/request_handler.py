from typing import ClassVar, Tuple, Optional
import time
import random
import os
import mimetypes
import requests

from .cacher import CacheManager, Cached, CacheCorrupted, CacheNotFound
from .logger import Logger


class RetryCounter:
    threshold: ClassVar[int] = 5

    def __init__(self) -> None:
        self._counter = 0

    def count(self) -> None:
        self._counter += 1
        Logger.info(f"One retry happened")
        if self._counter > 0.8 * self.threshold:
            Logger.warning(f"Retry counter close to limits")

    def reset(self) -> None:
        self._counter = 0

    def shouldContinue(self) -> bool:
        return self._counter < self.threshold

    def isFirstTime(self) -> bool:
        """
        Help determine if cache should be used or ignored

        Returns:
            bool: _description_
        """
        return self._counter == 0

    class RetryLimitReached(Exception):
        pass

class RequestError:
    class UnsuccessfulStatusCode(Exception):
        pass

    class EmptyResponseContent(Exception):
        pass

    class ConnectionError(Exception):
        pass

    class Unknown(Exception):
        pass


class RequestHandler:
    """Handling request globally so that the request rate would not exceed the server limit

    Raises:
        UnknownError: Some goofy error that beyond comprehension
    """
    retrieve_interval: ClassVar[Tuple[float, float]] = (5,1) # Mu, Sigma

    # Caching system
    _cacher: ClassVar[CacheManager] = CacheManager()

    _last_request_time: ClassVar[float] = time.time()

    @classmethod
    def setup(
        cls,
        mu: float = 5., 
        sigma: float = 1.,
        ) -> None:
        """Update the global parameters of RequestHandler

        Args:
            mu (float, optional): retrieval interval parameter, meaning average. Defaults to 5..
            sigma (float, optional): retrieval interval parameter, meaning variance. Defaults to 1..
        """
        cls.retrieve_interval = (mu, sigma)

    @classmethod
    def get_unhandled(cls, URL: str) -> requests.Response:
        """Try make a request and generate corresponding error code

        Args:
            URL (str): The URL to retrieve

        Raises:
            RequestError.UnsuccessfulStatusCode: Not 200 is bad
            RequestError.Unknown: WHAT? HOW?
            RequestError.EmptyResponseContent: Response does not contain a valid text field

        Returns:
            requests.Response: The only thing we are dreaming of
        """
        # Try making the request
        try:
            response = requests.get(
                        URL,
                        verify=True,
                        timeout=10,
                        )
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            Logger.error(f"Failed to connect to host server, because of {e}")
            raise RequestError.ConnectionError
        else:
            Logger.debug("Got a response.")
        finally:
            # Update timer
            cls._last_request_time = time.time()

        # Challenging response
        if (status_code:= response.status_code) != 200:
            Logger.warning(f"Abnormal response status code {status_code} from {URL}")
            raise RequestError.UnsuccessfulStatusCode

        if not isinstance(response, requests.Response):
            Logger.warning(f"Invalid response from {URL}")
            raise RequestError.Unknown

        if not response.text:
            Logger.warning(f"Empty response from {URL}")
            raise RequestError.EmptyResponseContent

        # Return successful ones
        return response

    @classmethod
    def get(cls, URL: str, ignoreCache: bool = False, file_extension_hint: str = "html", cache_time_to_live: Optional[int] = None) -> str:
        """Main API, get some URL

        Args:
            URL (str): the URL to get

        Raises:
            UnknownError: some goofy errors beyond comprehension

        Returns:
            str: the result of the GET in a string format
        """
        # --------------- Cache System ----------------------
        try:
            result = cls._cacher[URL]
        except CacheCorrupted:
            Logger.info(f"Corrupted cache encountered for {URL}, proceed with normal retrieval")
        except CacheNotFound:
            Logger.info(f"Cache file missing for {URL}")
        else:
            isCacheHit: bool = not ignoreCache

            if result.isExpired:
                Logger.debug(f"Cache miss due to cache expire")
                isCacheHit = False

            if isCacheHit:
                return result.content_str
        # --------------- Cache System ----------------------

        # Handle retry
        rc = RetryCounter()
        while rc.shouldContinue():
            # response: Optional[requests.Response] = None
            
            # Sleep till it is ok to retrieve
            cls.sleep()
            
            # Try making the request
            try:
                response = cls.get_unhandled(URL)
            except (RequestError.EmptyResponseContent, RequestError.UnsuccessfulStatusCode, RequestError.ConnectionError ,RequestError.Unknown):
                Logger.warning(f"Request failed, retrying")
                pass
            else:
                Logger.debug(f"Successfully get {URL}")

                # --------------- Cache System ----------------------
                extension_name = cls.extension_gusser(URL, response, default=file_extension_hint)
                Logger.debug(f"Best extension: {extension_name}")
                cache = Cached.from_content(
                    identifier = URL,
                    content = response.text,
                    time_to_live = cache_time_to_live,
                    file_extension = extension_name,
                )
                cls._cacher.append(cache)
                # --------------- Cache System ----------------------

                return response.text
            
            rc.count()
        
        # Finish retry loop
        raise RetryCounter.RetryLimitReached

    @classmethod
    def sleep(cls) -> None:
        """Keep the pace of the request
        """
        # Sleep till it is gut
        interval = random.gauss(cls.retrieve_interval[0], cls.retrieve_interval[1]) 
        if time.time() - cls._last_request_time < interval:
            time_to_sleep = cls._last_request_time + interval - time.time()
            Logger.debug(f"Time to sleep is {time_to_sleep}")
            time.sleep(time_to_sleep)
        return
    
    @staticmethod
    def extension_gusser(URL: Optional[str] = None, response: Optional[requests.Response] = None, default: str = "") -> str:
        """
        Guess the extension name based on URL and response, fallback to default when fail to guess

        Args:
            URL (Optional[str], optional): The URL where the file is from. Defaults to None.
            response (Optional[requests.Response], optional): The response from Get the URL. Defaults to None.
            default (str, optional): The default file extension name. Defaults to "".

        Returns:
            str: The guessed extension name, e.g. "html", "txt"
        """
        extension_name_guess_1 = ""
        extension_name_guess_2 = ""
        if URL:
            _, extension_name_guess_1 = os.path.splitext(URL)
            Logger.debug(f"Ext based on URL: {extension_name_guess_1}")

        if response:
            content_type = response.headers['Content-Type']
            extension_name_guess_2 = mimetypes.guess_extension(content_type)
            Logger.debug(f"Ext based on response: {extension_name_guess_2}")

        if extension_name_guess_1 == extension_name_guess_2 and extension_name_guess_1:
            # Best scenario
            extension_name = extension_name_guess_1
        elif extension_name_guess_2:
            # Use MIME first
            extension_name = extension_name_guess_2
        elif extension_name_guess_1:
            # Then URL
            extension_name = extension_name_guess_1
        else:
            # Last resort
            extension_name = default
        return extension_name

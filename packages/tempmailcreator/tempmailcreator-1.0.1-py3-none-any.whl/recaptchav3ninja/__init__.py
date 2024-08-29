from .ninja import Functions

class Ninja:
    """
    Main class that handles both synchronous and asynchronous operations for interacting 
    with the reCAPTCHA V3 service. Contains nested classes for both sync and async methods.
    """
    class Sync:
        """
        Handles synchronous interactions with the reCAPTCHA service.
        Contains a nested `Add` class and a static `run` method.
        """
        class Add:
            """
            Represents a configuration class for initializing reCAPTCHA-related parameters.
            The values for 'ar', 'k', 'co', 'hl', 'v', 'size', and 'cb' can either be passed
            directly or extracted from a URL if one is provided.

            Attributes:
                ar (int): Custom parameter for reCAPTCHA.
                k (str): reCAPTCHA site key.
                co (str): Country code parameter for reCAPTCHA.
                hl (str): Language code for reCAPTCHA (default is "en").
                v (str): Version of reCAPTCHA.
                size (str): Size of the reCAPTCHA (default is "invisible").
                cb (str): Callback parameter.
                url (str): URL from which parameters can be extracted.
                proxy (dict): Proxy configuration for requests.
                user_agent (str): The User-Agent string for HTTP headers.
            """
            def __init__(self, ar: int = None, k: str = None, co: str = None, hl: str = "en", v: str = None, size: str = "invisible", cb: str = None, url: str = None, proxy=None, user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Avast/126.0.0.0') -> None:
                """
                Initializes the Add instance with either the provided parameters or by 
                extracting the parameters from the given URL.

                Args:
                    ar (int, optional): Parameter 'ar' for reCAPTCHA.
                    k (str, optional): Site key for reCAPTCHA.
                    co (str, optional): Country code for reCAPTCHA.
                    hl (str, optional): Language code (default is "en").
                    v (str, optional): Version of reCAPTCHA.
                    size (str, optional): Size of reCAPTCHA (default is "invisible").
                    cb (str, optional): Callback function for reCAPTCHA.
                    url (str, optional): URL to extract parameters from (overrides individual parameters).
                    proxy (dict, optional): Proxy configuration for the request.
                    user_agent (str, optional): User-Agent header for the request.
                """
                self.ar = ar
                self.k = k
                self.co = co
                self.hl = hl
                self.v = v
                self.size = size
                self.cb = cb
                self.url = url
                self.proxy = proxy
                self.user_agent = user_agent
                if not url:
                    if any(param is None for param in [ar, k, co, hl, v, size, cb]):
                        raise ValueError("If the URL is not provided, all other parameters cannot be None.")
                else:
                    self._url(url)

            def _url(self, url):
                """
                Parses the URL to extract the reCAPTCHA parameters.

                Args:
                    url (str): The URL from which to extract the parameters.
                """
                parsed_url = Functions._url_ext(url)
                self.ar = parsed_url.get("ar", self.ar)
                self.k = parsed_url.get("k", self.k)
                self.co = parsed_url.get("co", self.co)
                self.hl = parsed_url.get("hl", self.hl)
                self.v = parsed_url.get("v", self.v)
                self.size = parsed_url.get("size", self.size)
                self.cb = parsed_url.get("cb", self.cb)
        @staticmethod
        def run(add_instance: 'Ninja.Sync.Add'):
            """
            Executes the synchronous reCAPTCHA process by creating an instance of SyncV3.

            Args:
                add_instance (Ninja.Sync.Add): An instance of the Add class with the necessary configuration.

            Returns:
                str: The final reCAPTCHA token after processing.
            """
            instance = Functions.SyncV3(
                ar=add_instance.ar,
                k=add_instance.k,
                co=add_instance.co,
                hl=add_instance.hl,
                v=add_instance.v,
                size=add_instance.size,
                cb=add_instance.cb,
                proxy=add_instance.proxy,
                user_agent=add_instance.user_agent
            )
            return instance._get_token()

    class Async:
        """
        Handles asynchronous interactions with the reCAPTCHA service.
        Contains a nested `Add` class and a static `run` method.
        """
        class Add:
            """
            Represents a configuration class for initializing reCAPTCHA-related parameters 
            asynchronously. The values for 'ar', 'k', 'co', 'hl', 'v', 'size', and 'cb' 
            can either be passed directly or extracted from a URL if one is provided.

            Attributes:
                ar (int): Custom parameter for reCAPTCHA.
                k (str): reCAPTCHA site key.
                co (str): Country code parameter for reCAPTCHA.
                hl (str): Language code for reCAPTCHA (default is "en").
                v (str): Version of reCAPTCHA.
                size (str): Size of the reCAPTCHA (default is "invisible").
                cb (str): Callback parameter.
                url (str): URL from which parameters can be extracted.
                proxy (dict): Proxy configuration for requests.
                user_agent (str): The User-Agent string for HTTP headers.
            """
            def __init__(self, ar: int = None, k: str = None, co: str = None, hl: str = "en", v: str = None, size: str = "invisible", cb: str = None, url: str = None, proxy=None, user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Avast/126.0.0.0') -> None:
                """
                Initializes the Add instance asynchronously with either the provided parameters or by 
                extracting the parameters from the given URL.

                Args:
                    ar (int, optional): Parameter 'ar' for reCAPTCHA.
                    k (str, optional): Site key for reCAPTCHA.
                    co (str, optional): Country code for reCAPTCHA.
                    hl (str, optional): Language code (default is "en").
                    v (str, optional): Version of reCAPTCHA.
                    size (str, optional): Size of reCAPTCHA (default is "invisible").
                    cb (str, optional): Callback function for reCAPTCHA.
                    url (str, optional): URL to extract parameters from (overrides individual parameters).
                    proxy (dict, optional): Proxy configuration for the request.
                    user_agent (str, optional): User-Agent header for the request.
                """
                self.ar = ar
                self.k = k
                self.co = co
                self.hl = hl
                self.v = v
                self.size = size
                self.cb = cb
                self.url = url
                self.proxy = proxy
                self.user_agent = user_agent
                
                if not url:
                    if any(param is None for param in [ar, k, co, hl, v, size, cb]):
                        raise ValueError("If the URL is not provided, all other parameters cannot be None.")
                else:
                    self._url(url)

            def _url(self, url):
                """
                Parses the URL to extract the reCAPTCHA parameters asynchronously.

                Args:
                    url (str): The URL from which to extract the parameters.
                """
                parsed_url = Functions._url_ext(url)
                self.ar = parsed_url.get("ar", self.ar)
                self.k = parsed_url.get("k", self.k)
                self.co = parsed_url.get("co", self.co)
                self.hl = parsed_url.get("hl", self.hl)
                self.v = parsed_url.get("v", self.v)
                self.size = parsed_url.get("size", self.size)
                self.cb = parsed_url.get("cb", self.cb)


        @staticmethod
        async def run(add_instance: 'Ninja.Async.Add'):
            """
            Executes the asynchronous reCAPTCHA process by creating an instance of AsyncV3.

            Args:
                add_instance (Ninja.Async.Add): An instance of the Add class with the necessary configuration.

            Returns:
                str: The final reCAPTCHA token after processing.
            """
            instance = Functions.AsyncV3(
                ar=add_instance.ar,
                k=add_instance.k,
                co=add_instance.co,
                hl=add_instance.hl,
                v=add_instance.v,
                size=add_instance.size,
                cb=add_instance.cb,
                proxy=add_instance.proxy,
                user_agent=add_instance.user_agent
            )
            return await instance._get_token()

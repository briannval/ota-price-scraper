import threading

from selenium import webdriver as wd
from selenium_stealth import stealth


class OtaDriver(object):
    """
    Singleton Selenium Webdriver to allow reusing
    """

    _instance = None

    @classmethod
    def get_driver(cls):
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
            cls._instance._initialize_driver()
        return cls._instance.__driver

    def __init__(self):
        raise RuntimeError("This is a singleton pattern, invoke get_driver() instead")

    def _initialize_driver(self):
        chrome_options = wd.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--ignore-certificate_errors")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_experimental_option("detach", True)
        driver = wd.Chrome(options=chrome_options)

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        self.__driver = driver

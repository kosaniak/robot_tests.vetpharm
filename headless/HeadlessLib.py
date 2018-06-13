from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver import ChromeOptions, FirefoxOptions


STR_TYPES = str, unicode


class HeadlessLib:
    """A helper library for opening web browsers in headless mode.
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self, selenium_lib_name='SeleniumLibrary', lib_instance=None):
        """HeadlessLib can be imported with one optional argument.

        If you use ``SeleniumLibrary``, you can simply:
        | Import Library | HeadlessLib |

        If you use Selenium2Library instead,
        provide the name of the library as the first argument:

        | Import Library | HeadlessLib | Selenium2Library |
        """
        if lib_instance:
            self._selenium_lib = lib_instance
            self._selenium_lib_name = lib_instance.__name__
        else:
            self._selenium_lib = None
            self._selenium_lib_name = selenium_lib_name

    @property
    def sl(self):
        """Lazy getter for library instance

        This is a workaround for situations when an instance of SeleniumLibrary
        does not yet exist.
        """
        if not self._selenium_lib:
            self._selenium_lib = BuiltIn().get_library_instance(
                    self._selenium_lib_name)
        return self._selenium_lib

    def open_headless_browser(self, browser, **kwargs):
        """Open the given browser in headless mode.

        Arguments:
        | browser | Name of the browser. |
        Supported values for ``browser`` are ``Firefox`` and ``Chrome``.
        """
        if not isinstance(browser, STR_TYPES):
            raise TypeError('expected one of %s, got %s' %
                            (STR_TYPES, type(browser)))
        if browser.lower() == 'firefox':
            return self.open_headless_firefox(**kwargs)
        elif browser.lower() == 'chrome':
            return self.open_headless_chrome(**kwargs)
        else:
            raise ValueError('unknown headless browser: %s' % browser)

    def open_headless_firefox(self, **kwargs):
        """Open Firefox in headless mode.
        """
        options = FirefoxOptions()
        options.set_headless()
        return self.sl.create_webdriver('Firefox', options=options, **kwargs)

    def open_headless_chrome(self, **kwargs):
        """Open Chrome / Chromium in headless mode.
        """
        options = ChromeOptions()
        options.set_headless()
        return self.sl.create_webdriver('Chrome', options=options, **kwargs)

*** Settings ***
Library  HeadlessLib.py  Selenium2Library
Library  Selenium2Library
Library  vetdoc.VetDocHomePage
Documentation  This suite tests the operation of several browsers in headless mode
...            (without any visible GUI and windows)


*** Variables ***
${BROWSER}  Firefox


*** Test Cases ***
First
  Open Selected Browser


*** Keywords ***
Open Selected Browser
  # [Documentation]  Open the browser of user's choice.
  Open Headless Browser  ${BROWSER}  alias=${BROWSER}
  Go To  ${BASEURL}
  Capture Page Screenshot
  Set Window Size  1920  1080
  Capture Page Screenshot
  Close Browser


# Firefox Headless
#   # [Documentation]  Tests the operation of Firefox browser in headless mode.
#   [Setup]          Open Headless Firefox  alias=Firefox
#   [Teardown]       Close Browser
#   Go To  https://quintagroup.com/
#   Capture Page Screenshot
#   Set Window Size  1920  1080
#   Capture Page Screenshot


# Chrome Headless
#   # [Documentation]  Tests the operation of Chrome / Chromium browser in headless mode.
#   [Setup]          Open Headless Chrome  alias=Chrome
#   [Teardown]       Close Browser
#   Go To  https://quintagroup.com/
#   Capture Page Screenshot
#   Set Window Size  1920  1080
#   Capture Page Screenshot

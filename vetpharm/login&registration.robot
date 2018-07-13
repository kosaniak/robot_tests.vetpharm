*** Settings ***
Documentation  Tests for https://vetpharm.fr

Library  vet_pharm.py
Library  vet_pharm.VetoPharmHomePage
Library  ../headless/HeadlessLib.py  vet_pharm.VetoPharmHomePage
Variables  ../vetpharm/sensitive_settings.py

Suite Teardown  Close Browser

*** Test Cases ***
Open VetoPharm homepage
    Open VetoPharm
    Set Window Size  1920  1080

Test if login works for correct credentials
    Login Into User Account

Find a vet
    Find A Vet
    Find A Vet With Advanced Research

Add a vet
    Add Found Vet

Delete the vet
    Delete Added Vet From Health Center
    Logout From Account

Test inability to login with incorrect credentials
    Try To Login With Incorrect Credentials

Test inability to register account with invalid email
    Try To Register The Invalid Email

Test inability to register account with already registered email
    Try To Register Already Taken Email

Test inability to register accont using too short password
    Use Too Short Password

Test if password confirmation works
    Unsuccessful Password Confirmation

Test if registration works
    ${password}=  register_account  ${register_email}
    Set Suite Variable  ${password}

Delete account
    Delete profile  ${password}

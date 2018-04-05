*** Settings ***
Documentation  Tests for http://vet-directory.devel.vetopharm.quintagroup.com/en/clinics/clinic/
...
Library  vetdoc.py
Library  vetdoc.VetDocHomePage

Suite Teardown  Close Browser

*** Test Cases ***

Open 'Clinic profile' page
    Open VetDoc
    Switch Between Clinics And Veterinarians
    ${clinic name}=  clinic_value
    Search By Name  ${clinic name}

Test whether language can be switched
    Switch Between Languages

Whether map is displayed
    Show Map  address map

Whether species/specialty are clickable with corresponding search results
    Check Species Option
    Back To Previous Page

Whether clinics' names are clickable and lead to profiles
    Open Veterinarian Profile

# Whether correct phone number is displayed on the page and in application
#     Check Contact Number

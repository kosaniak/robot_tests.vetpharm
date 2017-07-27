*** Settings ***
Documentation  Tests for http://vet-directory.devel.vetopharm.quintagroup.com/en/veterinarians/veterinarian/
...
Library  vetdoc.py
Library  vetdoc.VetDocHomePage

Suite Teardown  Close Browser

*** Test Cases ***

Open 'Veterinary profile' page
    Open VetDoc
    Maximize Browser Window
    ${veterinarian name}=  veterinarian_value
    Search By Name  ${veterinarian name}

Test whether language can be switched
    Switch Between Languages

Whether map is displayed
    Show Map  address map

Whether species/specialty are clickable with corresponding search results
    Check Species Option
    Back To Previous Page

Whether veterinarians' names are clickable and lead to profiles
    Open Clinic Profile

Whether correct phone number is displayed on the page and in application
    Check Contact Number

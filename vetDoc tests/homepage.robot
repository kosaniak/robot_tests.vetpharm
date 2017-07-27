*** Settings ***
Documentation  Tests for http://vet-directory.devel.vetopharm.quintagroup.com/
...
Library  vetdoc.py
Library  vetdoc.VetDocHomePage

Suite Teardown  Close Browser

*** Test Cases ***

Open 'Find a vet' home page
    Open VetDoc
    Maximize Browser Window

Test whether language can be switched
    Switch Between Languages

Test whether Address autocomplete works
    Search By Address
    Clear Address Field

Test whether name autocomplete works
    ${veterinarian name}=  veterinarian_value
    Search By Name  ${veterinarian name}
    Back To Previous Page
    Clear Name Field

Test whether it is possible to switch between Clinic and Veterinarian in the Name search field
    Switch Between Clinics And Veterinarians

Test whether clinic autocomplete works
    ${clinic name}=  clinic_value
    Search By Name  ${clinic name}
    Back To Previous Page
    Clear Name Field

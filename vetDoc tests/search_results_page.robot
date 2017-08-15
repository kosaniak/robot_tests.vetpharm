*** Settings ***
Documentation  Tests for http://vet-directory.devel.vetopharm.quintagroup.com/en/search/?pageNumber=0?show=Veterinarians
...
Library  vetdoc.py
Library  vetdoc.VetDocHomePage

Suite Teardown  Close Browser

*** Test Cases ***

Open Search results page
    Open VetDoc

Whether language can be switched
    Switch Between Languages

Whether map is displayed
    Show Map  location map

Whether distance filter works
    Check Distance Filter
    Clear Address Field

Whether Address autocomplete works
    Search By Address

Whether address info includes distance from the search location
    Show Distance From Location
    Clear Address Field

Whether Name autocomplete and search by name works
    ${veterinarian name}=  veterinarian_value
    Search By Name  ${veterinarian name}
    Back To Previous Page
    Clear Name Field

Whether it is possible to switch between Clinic and Veterinarian in the Name search field
    Switch Between Clinics And Veterinarians

Whether Clinic autocomplete and search by Clinic works
    ${clinic name}=  clinic_value
    Search By Name  ${clinic name}
    Back To Previous Page
    Clear Name Field

Whether species option is working
    Search By Species
    Clear Search Filter  species

Whether specialty option is working
    Search By Specialty
    Clear Search Filter  specialty

Test Clear All button
    Search By Specialty
    Clear All Search Filters

Test “Show Veterinarian/Clinic” drop-down
    Switch To Clinic Search

Whether changing language resets filter settings
    Search By Species
    Select French Language
    Check If Search Filters Are Cleared

Whether clinics’/veterinarians’ names are clickable and lead to profiles
  Go To Selected Profile

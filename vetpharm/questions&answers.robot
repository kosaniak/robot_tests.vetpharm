*** Settings ***
Documentation  Tests for https://vet-pharm.devel.vetopharm.quintagroup.com/en-gb/qa/questions/list

Resource  keywords.robot
Library  vet_pharm.VetoPharmHomePage
Library  ../headless/HeadlessLib.py  vet_pharm.VetoPharmHomePage
Variables  ../vetpharm/sensitive_settings.py

Suite Teardown  Close Browser

*** Test Cases ***
Open VetoPharm homepage
    Open VetoPharm
    Set Window Size  1920  1080

#--------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------

Log in as an admin user
    Login into admin account  ${email}  ${password}
    Go from dashboard to Q&A page

Go to Q&A page and send a question
    Submit a question

Check added question and its status
    ${last_question} =  Check added question message
    Check added question details  ${last_question}
    Set Suite Variable  ${last_question}

Approve the question
    View question  ${last_question}
    Approve question

Add English species tags
    @{english_tags} =  Create List
    Set Suite Variable  ${english_tags}
    ${english_tags} =  Add tag  ${english_tags}  5  id_tags_species_eng

Add English for who tags
    ${english_tags} =  Add tag  ${english_tags}  4  id_tags_for_who_eng

Add English indications tags
    ${english_tags} =  Add tag  ${english_tags}  3  id_tags_indications_eng

Add English substances tags
    ${english_tags} =  Add tag  ${english_tags}  3  id_tags_active_substances_eng

Add French species tags
    @{french_tags} =  Create List
    Set Suite Variable  ${french_tags}
    ${french_tags} =  Add tag  ${french_tags}  5  id_tags_species_fr

Add French for who tags
    ${french_tags} =  Add tag  ${french_tags}  4  id_tags_for_who_fr


Add French indications tags
    ${french_tags} =  Add tag  ${french_tags}  2  id_tags_indications_fr

Add French substances tags
    ${french_tags} =  Add tag  ${french_tags}  3  id_tags_active_substances_fr

Approve question and add answer
    Choose displaying question and approve it
    Add answer

Check question
    Go from dashboard to Q&A page
    Find answer

Check English tags
    Compare added and displayed tags  ${english_tags}

Check French tags
    Select French Language
    Compare added and displayed tags  ${french_tags}
    Select English Language

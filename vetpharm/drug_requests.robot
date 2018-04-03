*** Settings ***
Documentation  Tests for https://vetpharm.fr

Library  vet_pharm.py
Library  vet_pharm.VetoPharmHomePage
Variables  ../vetpharm/sensitive_settings.py

Suite Teardown  Close Browser

*** Test Cases ***

Open VetoPharm homepage
    Open VetoPharm
    Maximize Window

Add a drug request with one product as unlogged user
    Add drug request as guest user

Add comments to drug request and set "Rejected" status
    Add comments to drug request and check rejected status

Write comments to drug request and product and set its quantity limitation
    Write comments and set quantity limitation

Proceed to checkout as guest
    Proceed to checkout with paybox payment

Delete drug request after one-product purchase
    Delete drug request at dashboard
    Return To Site

Add a drug request with many products as logged in user
    ${list_of_chosen_prods}=  Add a drug request as logged in user
    Set Suite Variable  ${list_of_chosen_prods}

Remove product and change quantity in drug request
    Edit created drug request  ${list_of_chosen_prods}

Set "Approved" status to the edited drug request
    Set 'Approved' drug request status

Proceed to checkout with shipping method limitation
    Proceed to checkout with shipping method limitation

Delete drug request after multiple-product purchase
    Delete drug request at dashboard
    Return To Site

Write a review to a product
    Write a review and evaluate product

Edit a review to a product
    Edit a review

Delete a review to a product
    Delete a review

Logout from account
    Logout from account
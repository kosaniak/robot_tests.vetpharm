*** Settings ***
Documentation  Tests for https://vetpharm.fr

Library  vet_pharm.py
Library  vet_pharm.VetoPharmHomePage
Variables  ../vetpharm/sensitive_settings.py

Suite Teardown  Close Browser

*** Test Cases ***

Open VetoPharm homepage
    Open VetoPharm
    Set Window Size  1920  1080

Test if language can be selected
    Switch Between Languages

Test if currency can be selected
    Select Currency

Test if shippping country can be selected
    Select Shipping Country

Test if prices view can be selected
    Select Prices View

Register a new account
    register_account  ${register_email}

Add product to wishlist from listing and delete it
    Add product to wishlist from listing
    Update quantity in whishlist
    Delete product from wishlist

Add product to wishlist from product page and remove it
    Add product to wishlist from product page
    Delete product from wishlist

Add product to wishlist from recently viewed products
    Add product to wishlist from recently viewed
    Delete product from wishlist

Add product to wishlist after redirect bovi-pharm
    Redirect to purchase from bovi-pharm

Create and delete wishlist
    Create New Wishlist
    Delete The Wishlist

Add product to basket from listing and remove it
    Add product to basket
    Remove product from basket

Add product to basket from preview page and remove it
    Add product to basket from preview
    Remove product from basket

Add product to basket from recently viewed products and remove it
    Add product to basket from recently viewed products
    Remove product from basket

Log out from new account
    Logout From Account

Log into new account
    [tags]  log_into_new_account
    Open VetoPharm
    Maximize Window
    ${created_account_status}=  successful_login_into_new_account
    Set Suite Variable  ${created_account_status}

Delete account
    [tags]  delete_new_account
    Pass Execution If  '${created_account_status}' == 'False'  'Account has been not created'
    Delete profile  ${register_password}

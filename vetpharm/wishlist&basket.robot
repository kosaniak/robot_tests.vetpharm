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

Test if language can be selected
    Switch Between Languages

Test if currency can be selected
    Select Currency

Test if shippping country can be selected
    Select Shipping Country

Test if prices view can be selected
    Select Prices View

Register a new account
    ${account_password}=  register_account  ${register_email}
    Set Suite Variable  ${account_password}

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

Delete account
    Delete profile  ${account_password}
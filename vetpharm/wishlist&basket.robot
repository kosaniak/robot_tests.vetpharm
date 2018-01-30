*** Settings ***
Documentation  Tests for https://vetpharm.fr

Library  vet_pharm.py
Library  vet_pharm.VetoPharmHomePage

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
    ${password}=  register_account  testnotification@vetpharm.fr
    Set Suite Variable  ${password}

Add and delete product from whishlist
    Add product to wishlist
    Update quantity in whishlist
    Delete product from wishlist

Create and delete wishlist
    Create New Wishlist
    Delete The Wishlist

Add and remove product from basket
    Add product to basket
    Remove product from basket

Delete account
    Delete profile  ${password}

Proceed to checkout as logged in user
    Add product to basket
    Proceed to checkout as logged in user

Proceed to checkout as guest
    Add product to basket
    Proceed to checkout as guest

Proceed to checkout and create account
    Add product to basket
    Proceed to checkout and create account
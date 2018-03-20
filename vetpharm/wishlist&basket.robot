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

Proceed to checkout as logged in user
    Add product to basket
    Proceed to checkout as logged in user

Proceed to checkout as guest with payment during pickup
    Add product to basket from preview
    Checkout as guest with payment during pickup

Proceed to checkout and create account
    Add product to basket
    Proceed to checkout and create account

Proceed to checkout with excluding VAT payment
    Add product to basket from preview  2
    Add product to basket from preview  5
    Proceed to checkout excluding vat

Verify unreferenced product label in search results
    Verify unreferenced product label

Verify unreferenced product label for the manufacture of medicated feeds
    Verify unreferenced product label for the manufacture of medicated feeds

Verify manufactoring suspended label in search results
    Verify manufactoring suspended label

Verify manufactoring stopped label in search results
    Verify manufactoring stopped label

Verify marketing authorisation suspended label in search results
    Verify marketing authorisation suspended label

Verify unavailable out of stock label in search results
    Verify unavailable out of stock label

Verify prescription required label in search results
    Verify prescription required label

Verify veterinary drugs label in search results
    Verify veterinary drugs label

Verify issuance on prescription label in search results
    Verify issuance on prescription label

Verify livestock health program filter in search results
    Verify livestock health program filter
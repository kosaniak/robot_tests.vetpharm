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

Proceed to checkout as logged in user
    Add product to basket
    Proceed to checkout as logged in user

Proceed to checkout as guest with payment during pickup
    Add product to basket from preview
    Checkout as guest with payment during pickup

Proceed to checkout with excluding VAT payment
    Add product to basket from preview  2
    Add product to basket from preview  5
    Proceed to checkout excluding vat

Proceed to checkout and create account
    Add product to basket
    Proceed to checkout and create account

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

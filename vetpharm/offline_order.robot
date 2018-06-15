*** Settings ***
Documentation  Tests for http://vet-directory.devel.vetopharm.quintagroup.com/en

Resource  keywords.robot
Library  vet_pharm.VetoPharmHomePage
Variables  ../vetpharm/sensitive_settings.py

Suite Teardown  Close Browser

*** Test Cases ***
Open VetoPharm homepage
    Open VetoPharm
    Set Window Size  1920  1080

#--------------------------------------------------------------------------------------
#  Place order with existing user and checking search filters
#--------------------------------------------------------------------------------------

Create a new user for offline order
    Create a new user and log out

Log in as an admin user
    Login into admin account  ${email}  ${password}

Start creating order by phone
    Fill out offline order info  ${order_by_phone}

Check user search by email
    ${search_results_length} =  Search user by email  sorenabell@quintagroup.com  ${choose_user.email_filter_results}
    Check reseting search filter  ${choose_user.reset_search_filter}  ${search_results_length}  ${choose_user.email_filter_results}

Check user search by name
    ${search_results_length} =  Search user by name
    Check reseting search filter  ${choose_user.reset_search_filter}  ${search_results_length}  ${choose_user.name_filter_results}

Choose user from search results
    Choose user

Check search filters in forming basket
    Form basket and search product by title
    Search product by laboratory
    Search product by CIP code
    Search product by UPC code

Add product to basket and remove it
    ${chosen_product}  ${chosen_prod_title} =  Choose product
    Change quantity and add product  ${chosen_product}  5
    Check basket  ${chosen_prod_title}  5
    Remove product from basket

Add a new product
    ${chosen_product}  ${chosen_prod_title} =  Choose product
    Change quantity and add product  ${chosen_product}  2
    Check basket  ${chosen_prod_title}  2

Add a new address and choose shipping method
    Scroll to element out of viewport  ${shipping}
    Click Element At Coordinates  ${shipping}  0  0
    Add shipping address
    Choose address from available ones  ${shipping.ship_to_address}  ${shipping.added_shipping_ad}
    Choose address from available ones  ${shipping.bill_to_address}  ${shipping.added_billing_ad}
    Choose shipping method

Add payment method
    Choose payment method

Add and delete shipping discounts in order preview
    ${shipping_price} =  Add absolute shipping discount
    Edit shipping discount to percentage  ${shipping_price}
    Edit shipping discount to fixed price and delete it  ${shipping_price}

Add order message and place order
    ${total_price_1} =  Add message before placing order
    Logout from account
    Set Suite Variable  ${total_price_1}

Check receiving confirmation letter to email
    Log into user e-mail  ${register_email}  ${register_password}
    Check letter with confirmation of order  Confi  ${check_email.confirmation_title}

Check sending payment information to email
    Check letter with payment information  Order  ${check_email.proceed_to_payment_btn}  ${total_price_1}

Proceed to payment from e-mail
    Log into new account and proceed to payment

Delete newly created account
    Log into new account
    Delete new account

#--------------------------------------------------------------------------------------
#  Place order with creation of a new user and shipping to excl vat area
#--------------------------------------------------------------------------------------

Return to admin account
    Go to  http://vet-pharm.devel.vetopharm.quintagroup.com
    Login into admin account  ${email}  ${password}

Start creating an offline order
    Fill out offline order info  ${purchase_at_pharmacy}

Add a new user while placing an order
    Add a new user

Begin creating an offline order
    Fill out offline order info  ${purchase_at_pharmacy}

Choose recently created user
    Click Element  ${add_order.choose_user}
    Choose user

Form basket for the order
    Click Element  ${form_basket}
    ${chosen_product}  ${chosen_prod_title} =  Choose product
    Change quantity and add product  ${chosen_product}  3
    Check basket  ${chosen_prod_title}  3

Check shipping address
    Check available shipping address
    Add shipping address
    Choose address from available ones  ${shipping.bill_to_address}  ${shipping.added_billing_ad}

Proceed to payment
    Choose payment method  ${True}

Add and delete basket discounts in order preview
    ${basket_price} =  Add percentage basket discount
    Edit basket discount to fixed price and delete it  ${basket_price}

Add message and place order
    Add message before placing order

Check sending invoice for order to email
    Log into user e-mail  ${register_email}  ${register_password}
    Check letter with invoice of order  Invoi  ${check_email.confirmation_title}

Delete inactive user account
    Go to customers list at dashboard
    Delete a user from dashboard  inactive+testnotification@vetpharm.fr
    Check user deletion  inactive+testnotification@vetpharm.fr

Delete active user account
    Delete a user from dashboard  testnotification@vetpharm.fr
    Check user deletion  testnotification@vetpharm.fr

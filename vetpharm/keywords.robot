*** Settings ***

Library  Selenium2Library
Library  String
Library  Collections
Library  vet_pharm.py
Library  vet_pharm.VetoPharmHomePage
Variables  ../vetpharm/sensitive_settings.py


Resource  locators.robot

*** Variables ***
${input_question_msg}  How much is delivery?
${question_submission_nofication}  Your question was asked successfully

*** Keywords ***
#--------------------------------------------------------------------------------------
#  Support keywords
#--------------------------------------------------------------------------------------
Open VetoPharm website
    Open VetoPharm
    Maximize Browser Window


Create a new user and log out
    Register new account  ${register_email}
    Sleep  4
    Logout from account


Login into admin account
    [Arguments]  ${email}  ${password}
    Click Element  ${login_or_register}
    Input Password  ${input_username}  ${email}
    Input Password  ${input_password}  ${password}
    Click Element  ${submit_login}
    Sleep  4


Go from dashboard to Q&A page
    Return to site
    Wait Until Element Is Visible  ${ask_question.q&a_button}
    Click Element  ${ask_question.q&a_button}


Go to dashboard from website
    Wait Until Element Is Visible  xpath=//div[@class='user-account']
    Mouse Over  xpath=//div[@class='user-account']
    Click Element  xpath=//div[@class='user-account']
    Click Element  xpath=//a[contains(text(),'Dashboard')]


Close chat box
    Capture Page Screenshot
    ${chatbox_is_visible} =  Run Keyword And Return Status  Element Should Be Visible  xpath=//a[@id='endChat']/span
    Run Keyword If  ${chatbox_is_visible}  Run Keywords
    ...     Mouse Over  xpath=//a[@id='endChat']/span
    ...     Click Element  xpath=//a[@id='endChat']/span
    Element Should Not Be Visible  //div[@id='chatPanel']

#--------------------------------------------------------------------------------------
#  Questions&Answers
#--------------------------------------------------------------------------------------

Submit a question
    Wait Until Element Is Visible  ${ask_question.ask_a_question_btn}
    Click Element  ${ask_question.ask_a_question_btn}
    Wait Until Element Is Visible  id=id_name
    Input Text  id=id_name  superuser
    Input Text  id=id_email  superuservetpharm@gmail.com
    Input Text  id=id_phone  +33 (0)3 81 60 35 06
    Input Text  id=id_message  ${input_question_msg}
    Click Element  ${ask_question.send_message}
    Page Should Contain  ${question_submission_nofication}


Check added question message
    Go to dashboard from website
    Wait Until Element Is Visible  ${customers_list}
    Click Element At Coordinates  ${customers_list}  0  0
    Sleep  1
    Click Element  xpath=//a[contains(text(),'Product Questions')]
    @{last_question} =  Get Webelements  ${ask_question.last_question}
    ${question_msg_elem} =  Get child webelement  ${last_question[0]}  .//td[1]//a
    ${found_question_message} =  Get Text  ${question_msg_elem}
    Should Be Equal As Strings  ${found_question_message}  ${input_question_msg}
    [Return]  ${last_question[0]}


Check added question details
    [Arguments]  ${last_question}
    ${question_author} =  Get child webelement  ${last_question}  .//td[2]
    ${found_question_author} =  Get Text  ${question_author}
    Should Be Equal As Strings  ${found_question_author}  superuser(superuservetpharm@gmail.com)
    ${question_phone} =  Get child webelement  ${last_question}  .//td[3]
    ${found_question_phone} =  Get Text  ${question_phone}
    Should Be Equal As Strings  ${found_question_phone}  +33 (0)3 81 60 35 06
    ${question_status} =  Get child webelement  ${last_question}  .//td[8]
    ${found_question_status} =  Get Text  ${question_status}
    Should Be Equal As Strings  ${found_question_status}  Processing


View question
    [Arguments]  ${last_question}
    ${view_question} =  Get child webelement  ${last_question}  .//a[@class='btn btn-primary']
    Click Element  ${view_question}
    Wait Until Element Is Visible  //h2[contains(text(), 'Question details')]


Approve question
    Scroll to element out of viewport  ${approve_question}
    Capture Page Screenshot
    Click Element  ${approve_question}
    Sleep  2
    Page Should Contain  Question's status was successfully changed


Add tag
    [Arguments]  ${list_of_tags}  ${range_of_limit}  ${tag_id}
    :FOR  ${index}  IN RANGE  1  ${range_of_limit}
    \   Click Element  id=s2id_${tag_id}
    \   Sleep  1
    \   ${tag_title} =  Choose tag  ${index}  //label[@for='${tag_id}']/..
    \   ${tag_title_lowercase} =  Convert To Lowercase  ${tag_title}
    \   Append To List  ${list_of_tags}  ${tag_title_lowercase}
    [Return]  ${list_of_tags}


Choose tag
    [Arguments]  ${tag_idex}  ${search_tag_result}
    ${chosen_tag} =  Choose element from list  ${tag.species_eng}
    ${tag_title} =  Get Text  ${chosen_tag}
    Scroll to element out of viewport  ${chosen_tag}
    Click Element  ${chosen_tag}
    Page Should Contain Element  xpath=//li[@class='select2-search-choice'][${tag_idex}]/div
    ${added_tag_title} =  Get Text  xpath=${search_tag_result}//li[@class='select2-search-choice'][${tag_idex}]/div
    Should Be Equal As Strings  ${tag_title}  ${added_tag_title}
    [Return]  ${tag_title}


Choose displaying question and approve it
    Scroll to element out of viewport  xpath=//*[@id='id_show_on_site']
    Click Element  id=id_show_on_site
    Click Element  id=s2id_id_sites_to_display
    Press Key  id=s2id_id_sites_to_display  vet-pharm
    Click Element  ${website_to_display}
    ${chosen_website} =  Get Text  ${chosen_website_to_diplay}
    Should Be Equal As Strings  ${chosen_website}  vet-pharm.devel.vetopharm.quintagroup.com
    Capture Page Screenshot
    Scroll to element out of viewport  ${ask_question.save}
    Click Element  ${ask_question.save}
    Capture Page Screenshot


Add answer
    Scroll to element out of viewport  ${add_answer}
    Click Element  ${add_answer}
    Wait Until Element Is Visible  id=id_answer_text_ifr
    Press Key  id=id_answer_text_ifr  It depends on the shipping method
    Click Element  ${ask_question.save}
    Sleep  4


Find answer
    Press Key  id=id_question  How much is delivery?
    Click Element  ${search_question}
    Sleep  3
    ${my_question} =  Get Webelements  ${found_question_in_list}
    ${view_btn} =  Get child webelement  ${my_question[0]}  ${view_found_question}
    Click Element  ${view_btn}
    Sleep  3
    Page Should Contain  How much is delivery?


Compare added and displayed tags
    [Arguments]  ${already_added_tags}
    @{displayed_tags_elements} =  Get Webelements  ${question_tag}
    @{displayed_tags} =  Create List
    :FOR  ${tag}  IN  @{displayed_tags_elements}
    \   ${tag_title} =  Get Text  ${tag}
    \   ${tag_title_lowercase} =  Convert To Lowercase  ${tag_title}
    \   Append To List  ${displayed_tags}  ${tag_title_lowercase}
    Compare Lists  ${already_added_tags}  ${displayed_tags}

#--------------------------------------------------------------------------------------
#  Order Info
#--------------------------------------------------------------------------------------

Fill out offline order info
    [Arguments]  ${order_type}
    Click Element  ${place_order}
    Wait Until Element Is Visible  ${order_type}
    Click Element  ${order_type}
    Sleep  2
    Click Element  ${add_order.reset_site}
    Sleep  1
    Click Element  ${add_order.select_site}
    Sleep  1
    Press Key  ${add_order.select_site}  vet-pharm
    Sleep  3
    Mouse Over  ${add_order.choose_site}
    Sleep  2
    Click Element At Coordinates  ${add_order.choose_site}  0  0
    Sleep  1
    ${website} =  Get Text  ${add_order.site}
    Should Be Equal As Strings  ${website}  vet-pharm.devel.vetopharm.quintagroup.com  'The chosen site is other than vet-pharm.devel.vetopharm.quintagroup.com'
    Sleep  2

#--------------------------------------------------------------------------------------
#  Choose User
#--------------------------------------------------------------------------------------

Add a new user
    Wait Until Element Is Visible  ${add_order.choose_user}
    Click Element  ${add_order.choose_user}
    Wait Until Element Is Visible  ${choose_user.add_new_user}
    Click Element  ${choose_user.add_new_user}
    Sleep  4
    Wait Until Element Is Visible  ${choose_user.email_input}
    Input Text  ${choose_user.email_input}  ${register_email}
    Input Text  ${choose_user.first_name_input}  John
    Input Text  ${choose_user.last_name_input}  Johnsons
    Scroll to element out of viewport  ${choose_user.type_of_customer}
    Click Element  ${choose_user.type_of_customer}
    Sleep  1
    Capture Page Screenshot
    Input text  ${choose_user.type_input}  ind
    Sleep  1
    Click Element  ${choose_user.individual_customer}
    Scroll to element out of viewport  ${save}
    Click Element  ${save}
    Sleep  5


Search user by email
    [Arguments]  ${user_email}  ${email_results}
    Run Keyword If  '${user_email}' == 'sorenabell@quintagroup.com'  Click Element  ${add_order.choose_user}
    Input Text  ${choose_user.email_input}  ${user_email}
    Click Element  ${choose_user.search_with_filter}
    Sleep  2
    @{results_list} =  Check search results  ${email_results}  ${user_email}
    ${search_results_length} =  Get Length  ${results_list}
    Sleep  3
    [Return]  ${search_results_length}


Search user by name
    Input Text  ${choose_user.first_name_input}  BEATRICE
    Input Text  ${choose_user.last_name_input}  ACHOUR
    Click Element  ${choose_user.search_with_filter}
    Sleep  2
    @{results_list} =  Check search results  ${choose_user.name_filter_results}  BEATRICE ACHOUR
    ${search_results_length} =  Get Length  ${results_list}
    Sleep  3
    [Return]  ${search_results_length}


Choose user
    Input Text  ${choose_user.email_input}  ${register_email}
    Click Element  ${choose_user.search_with_filter}
    Sleep  2
    ${index} =  Find necessary user index
    ${available_users} =  Get Webelements  ${choose_user_btn}
    Click Element  ${available_users[${index}]}
    Sleep  3
    ${chosen_user_email} =  Get Text  ${choose_user.email}
    Should Be Equal As Strings  ${chosen_user_email}  ${register_email}
    Sleep  2


Find necessary user index
    @{all_emails} =  Get Webelements  ${choose_user.email_filter_results}
    :FOR  ${email}  IN  @{all_emails}
    \   ${found_email} =  Get Text  ${email}
    \   ${index} =  Run Keyword If  '${found_email}' == '${register_email}'  Run Keyword And Return
    \   ...     Get Index From List  ${all_emails}  ${email}
    [Return]  ${index}


Check reseting search filter
    [Arguments]  ${reset_button}  ${search_results_length}  ${choose_user.filter_results}
    Click Element  ${reset_button}
    Sleep  2
    ${no_filter_list_length} =  Get Matching Xpath Count  ${choose_user.filter_results}
    Should Not Be Equal  ${search_results_length}  ${no_filter_list_length}
    Sleep  2

#--------------------------------------------------------------------------------------
#  Form Basket
#--------------------------------------------------------------------------------------

Form basket and search product by title
    Click Element  ${form_basket}
    Wait Until Element Is Visible  ${form_basket.search_by_title}  15
    Input Text  ${form_basket.search_by_title}  abcedyl
    Click Element  ${form_basket.search_button}
    Sleep  2
    Check search results with partial text  ${form_basket.by_title_result}  ABCEDYL  0
    Click Element  ${form_basket.reset_search_filters}
    Sleep  5


Search product by laboratory
    Input Text  ${form_basket.search_by_lab}  merial
    Click Element  ${form_basket.search_button}
    Sleep  2
    Check search results  ${form_basket.by_laboratory_results}  MERIAL
    Click Element  ${form_basket.reset_search_filters}
    Sleep  5


Search product by CIP code
    Input Text  ${form_basket.search_by_CIP_code}  8020380
    Click Element  ${form_basket.search_button}
    Sleep  2
    Check search results with partial text  ${form_basket.by_code_results}  8020380  1
    Click Element  ${form_basket.reset_search_filters}
    Sleep  5


Search product by UPC code
    Input Text  ${form_basket.search_by_UPC_code}  368879
    Click Element  ${form_basket.search_button}
    Sleep  2
    Check search results with partial text  ${form_basket.by_code_results}  368879  3
    Click Element  ${form_basket.reset_search_filters}
    Sleep  5


Choose product
    ${chosen_product} =  Choose element from list  ${form_basket.add_available_prod}
    Scroll to element out of viewport  ${chosen_product}
    ${title_box} =  Get child webelement  ${chosen_product}  ${form_basket.chosen_prod_title}
    ${chosen_prod_title} =  Get Text  ${title_box}
    [Return]  ${chosen_product}  ${chosen_prod_title}


Change quantity and add product
    [Arguments]  ${chosen_product}  ${quantity}
    ${quantity_box} =  Get child webelement  ${chosen_product}  ${form_basket.quantity_box}
    Input Text  ${quantity_box}  ${quantity}
    Sleep  1
    ${add_prod_btn} =  Get child webelement  ${chosen_product}  ${form_basket.add_to_order_btn}
    Click Element  ${add_prod_btn}
    Sleep  3


Check basket
    [Arguments]  ${chosen_prod_title}  ${added_quantity}
    Scroll to element out of viewport  ${form_basket.basket}
    Sleep  1
    ${added_prod_title} =  Get Text  ${form_basket.basket.added_prod_title}
    Should Be Equal As Strings  ${chosen_prod_title}  ${added_prod_title}
    ${quantity_in_basket} =  Get Text  ${form_basket.basket.added_quantity}
    Should Be Equal As Numbers  ${quantity_in_basket}  ${added_quantity}
    Sleep  2


Remove product from basket
    Scroll to element out of viewport  ${form_basket.basket.remove_product}
    Sleep  2
    Click Element  ${form_basket.basket.remove_product}
    Capture Page Screenshot
    Sleep  4
    Page Should Not Contain Element  ${form_basket.basket}  'Product has been not removed from basket'

#--------------------------------------------------------------------------------------
#  Shipping
#--------------------------------------------------------------------------------------

Check available shipping address
    Click Element  ${shipping}
    Click Element  ${shipping.input_method}
    Press Key  ${shipping.input_method}  pick
    Capture Page Screenshot
    Sleep  1
    Click Element  ${shipping.select_method}
    Sleep  1
    @{available_address} =  Get WebElements  //div[@class='col-md-6']//address
    Length Should Be  ${available_address}  1
    ${shipping_address} =  Get Text  ${shipping.select_address_pharmacy}
    Should Be Equal As Strings  ${shipping_address}  Pharmacie BASTARD


Add shipping address
    Wait Until Element Is Visible  ${shipping.add_address}
    Click Element  ${shipping.add_address}
    Wait Until Element Is Visible  ${shipping.add_address_modal}
    Input into autocomplete  ${shipping.autocomplete_address}  geneva
    Sleep  1
    Capture Page Screenshot
    Click Element  ${shipping.cannot_find_address_btn}
    Click Element  xpath=//span[@id='react-select-4--value']//div[@class='Select-placeholder']
    Press Key  xpath=//span[@id='react-select-4--value']//div[@class='Select-placeholder']  m
    Capture Page Screenshot
    Sleep  1
    ${chosen_title} =  Choose element from list  xpath=//div[@class='Select-menu-outer']//*
    Click Element  ${chosen_title}
    Sleep  2
    Press Key  xpath=//div[@class='address-form']//input[@id='id_first_name']  Jean
    Press Key  xpath=//div[@class='address-form']//input[@id='id_last_name']  Jeak
    Press Key  xpath=//div[@class='address-form']//input[@id='id_line1']  Place Dorciere
    Press Key  xpath=//div[@class='address-form']//input[@id='id_postcode']  1201
    Press Key  xpath=//div[@class='address-form']//input[@id='id_line4']  geneva
    Press Key  xpath=//div[@class='address-form']//input[@id='id_state']  GE
    Sleep  1
    Click Element  xpath=//label[@for='id_country']/..//div[@class='Select-placeholder']
    Press Key  xpath=//label[@for='id_country']/..//div[@class='Select-placeholder']  switzerland
    Sleep  1
    Click Element  xpath=//div[@class='Select-menu-outer']//*
    Sleep  2
    Capture Page Screenshot
    Mouse Over  ${shipping.autocomplete_submit}
    Click Element  ${shipping.autocomplete_submit}
    Sleep  1


Choose address from available ones
    [Arguments]  ${choose_address_btn}  ${added_address_block}
    Scroll to element out of viewport  ${choose_address_btn}
    Click Element  ${choose_address_btn}
    Sleep  2
    Element Should Be Visible  ${added_address_block}


Choose shipping method
    Scroll to element out of viewport  ${shipping.method_input}
    Click Element  ${shipping.method_input}
    Press Key  ${shipping.method_input}  livraison
    Mouse Over  ${choose_from_autocomplete}
    Click Element  ${choose_from_autocomplete}
    Sleep  2

#--------------------------------------------------------------------------------------
#  Payment
#--------------------------------------------------------------------------------------

Choose payment method
    [Arguments]  ${random_method}=${None}
    Click Element  ${payment}
    Sleep  2
    Click Element  ${payment.select_method}
    Press Key  ${payment.select_method}  credit
    ${method}=  Set Variable  ${None}
    ${method}=  Run Keyword If  '${random_method}' == '${True}'
    ...     Choose element from list  ${choose_from_autocomplete}
    ...     ELSE
    ...     Set Variable  ${payment.choose_credit_card}
    Capture Page Screenshot
    Click Element  ${method}
    Capture Page Screenshot
    Sleep  2

#--------------------------------------------------------------------------------------
#  Order Preview
#--------------------------------------------------------------------------------------

Add percentage basket discount
    Click Element  ${order_preview}
    Scroll to element out of viewport  ${order_preview.basket_summary_incl_tax}
    ${basket_price} =  Get Text  ${order_preview.basket_summary_incl_tax}
    Add price discount  percentage  ${order_preview.add_discount_to_basket}  ${order_preview.discount_type_autocomp}
    Check if discount has been applied  ${basket_price}  ${order_preview.basket_summary_incl_tax}
    [Return]  ${basket_price}


Edit basket discount to fixed price and delete it
    [Arguments]  ${basket_price}
    Edit added discount  fixed  ${order_preview.edit_discount_type}
    Check if discount has been applied  ${basket_price}  ${order_preview.basket_summary_incl_tax}
    Check basket price after discount deletion  ${basket_price}  ${order_preview.basket_summary_incl_tax}
    Page Should Not Contain Element  xpath=//td[@class='text-danger']


Add absolute shipping discount
    Click Element  ${order_preview}
    Scroll to element out of viewport  ${order_preview.shipping_summary_incl_tax}
    ${shipping_price} =  Get Text  ${order_preview.shipping_summary_incl_tax}
    Add price discount  absolute  ${order_preview.add_shipping_discount}  ${order_preview.shipping_discount_autocomp}
    Check if discount has been applied  ${shipping_price}  ${order_preview.shipping_summary_incl_tax}
    [Return]  ${shipping_price}


Edit shipping discount to percentage
    [Arguments]  ${shipping_price}
    Edit added discount  percentage  ${order_preview.edit_discount_type}
    Check if discount has been applied  ${shipping_price}  ${order_preview.shipping_summary_incl_tax}


Edit shipping discount to fixed price and delete it
    [Arguments]  ${shipping_price}
    Edit added discount  shipping  xpath=//span[@id='react-select-9--value']/div[1]
    Check if discount has been applied  ${shipping_price}  ${order_preview.shipping_summary_incl_tax}
    Check basket price after discount deletion  ${shipping_price}  ${order_preview.shipping_summary_incl_tax}
    Page Should Contain  YOUR ORDER IS EXEMPT FROM FRENCH VAT (VAT =


Add message before placing order
    Scroll to element out of viewport  ${order_preview.order_message}
    Input Text  ${order_preview.order_message}  Your order has been placed successfully
    Sleep  1
    ${total_price} =  Get Text  ${order_preview.total_price}
    ${price_only} =  Fetch From Right  ${total_price}  €
    Scroll to element out of viewport  ${order_preview.place_order}
    Sleep  1
    Click Element  ${order_preview.place_order}
    Sleep  8
    Page Should Contain Element  xpath=//div[@class='panel-title']
    Return to site
    Sleep  2
    [Return]  ${price_only}


Check letter with confirmation of order
    [Arguments]  ${letter_index}  ${title_el}
    Check e-mail letter  ${letter_index}  ${title_el}
    Page Should Contain Element  ${check_email.vat_exempt_msg}  The total price should be exempt from vat.
    Page Should Contain  Your order has been placed successfully  Pharmacist's message has been not added


Check letter with payment information
    [Arguments]  ${letter_index}  ${title_el}  ${total_price}
    Check e-mail letter  ${letter_index}  ${title_el}
    ${price_msg} =  Get Text  xpath=//div/p[4]/strong
    ${price_to_pay} =  Fetch From Right  ${price_msg}  €
    Should Be Equal As Numbers  ${total_price}  ${price_to_pay}  Total price is different in the e-mail


Check letter with invoice of order
    [Arguments]  ${letter_index}  ${title_el}
    Check e-mail letter  ${letter_index}  ${title_el}
    ${payment_status} =  Get Text  xpath=//div[@class='second_block']/strong[3]
    Should Be Equal As Strings  ${payment_status}  Paid  Payment status is other than Paid


Check e-mail letter
    [Arguments]  ${letter_title}  ${title_el}
    Find received letters  ${letter_title}
    Check email content  ${title_el}


Log into new account and proceed to payment
    Log into account from email
    Find received letters  Order
    Select Frame  id=messagecontframe
    Wait Until Element Is Visible  xpath=//img[@alt='Vet Pharm']
    Scroll to element out of viewport  ${check_email.proceed_to_payment}
    Sleep  2
    Click Element At Coordinates  ${check_email.proceed_to_payment}  0  0
    Sleep  5
    Close prev window tab
    Sleep  2
    Pay with paybox
    Wait Until Element Is Visible  ${order_preview.view_after_payment}
    Click Element  ${order_preview.view_after_payment}
    Sleep  4


Add price discount
    [Arguments]  ${discount_type}  ${add_discount_btn}  ${autocomp_box}
    Click Element  ${add_discount_btn}
    Wait Until Element Is Visible  ${autocomp_box}
    Input into autocomplete  ${autocomp_box}  ${discount_type}
    Sleep  3
    Click Element At Coordinates  ${choose_from_autocomplete}  0  0
    Sleep  2
    Press Key  ${order_preview.discount_input}  4
    Sleep  2
    Mouse Over  ${save}
    Click Element At Coordinates  ${save}  0  0
    Sleep  4


Edit added discount
    [Arguments]  ${discount_type}  ${autocomp_box}
    Scroll to element out of viewport  ${order_preview.edit_discount}
    Click Element  ${order_preview.edit_discount}
    Wait Until Element Is Visible  ${autocomp_box}
    Input into autocomplete  ${autocomp_box}  ${discount_type}
    Sleep  1
    Click Element  ${choose_from_autocomplete}
    Sleep  2
    Click Element  ${save}
    Sleep  4


Check if discount has been applied
    [Arguments]  ${initial_price}  ${total_price_box}
    Page Should Contain Element  xpath=//h5  'Discount has been not added'
    Scroll to element out of viewport  ${total_price_box}
    ${discounted_price} =  Get Text  ${total_price_box}
    Should Not Be Equal As Strings  ${initial_price}  ${discounted_price}
    Page Should Contain Element  xpath=//td[@class='text-danger']


Check basket price after discount deletion
    [Arguments]  ${initial_price}  ${total_price_box}
    Scroll to element out of viewport  ${order_preview.delete_discount}
    Click Element  ${order_preview.delete_discount}
    Sleep  3
    Page Should Not Contain Element  ${order_preview.delete_discount}
    Scroll to element out of viewport  ${total_price_box}
    ${total_without_discount} =  Get Text  ${total_price_box}
    Should Be Equal As Strings  ${initial_price}  ${total_without_discount}

#--------------------------------------------------------------------------------------
#  Delete Users from Dashboard
#--------------------------------------------------------------------------------------

Go to customers list at dashboard
    Go To  http://vet-pharm.devel.vetopharm.quintagroup.com/
    Go to dashboard from website
    Wait Until Element Is Visible  ${customers_list}
    Click Element At Coordinates  ${customers_list}  0  0
    Sleep  1
    Click Element  xpath=//a[contains(text(),'Customers')]


Delete a user from dashboard
    [Arguments]  ${user_email}
    Wait Until Element Is Visible  ${choose_user.email_input}
    Search user by email  ${user_email}  xpath=//td[@class='email']
    Click Element  ${delete_user}
    Wait Until Element Is Visible  ${confirm_user_deletion}
    Click Element  ${confirm_user_deletion}


Check user deletion
    [Arguments]  ${user_email}
    Wait Until Element Is Visible  ${choose_user.email_input}
    Input Text  ${choose_user.email_input}  ${user_email}
    Click Element  ${choose_user.search_with_filter}
    Sleep  2
    Page Should Contain  No customers found.
    Check reseting search filter  xpath=//a[contains(text(), 'Reset')]  '0'  ${choose_user.email_filter_results}

#--------------------------------------------------------------------------------------
#  Service_keywords
#--------------------------------------------------------------------------------------

Check search results
    [Arguments]  ${result_locator}  ${search_filter}
    @{results_list} =  Get WebElements  ${result_locator}
    :FOR  ${el}  IN  @{results_list}
    \   ${found_el} =  Get Text  ${el}
    \   Should Be Equal As Strings  ${found_el}  ${search_filter}
    Sleep  3
    [Return]  ${results_list}


Check search results with partial text
    [Arguments]  ${result_locator}  ${search_filter}  ${index}
    @{results_list} =  Get WebElements  ${result_locator}
    :FOR  ${el}  IN  @{results_list}
    \   ${found_el} =  Get Text  ${el}
    \   @{partial_text} =  Split String  ${found_el}
    \   Should Be Equal As Strings  ${partial_text[${index}]}  ${search_filter}
    Sleep  3
    [Return]  ${results_list}

Log into new account
    [tags]  log_into_new_account
    Open VetoPharm
    Maximize Window
    ${created_account_status}=  successful_login_into_new_account
    Set Suite Variable  ${created_account_status}


Delete new account
    [tags]  delete_new_account
    Pass Execution If  '${created_account_status}' == 'False'  'Account has been not created'
    Delete profile  ${register_password}

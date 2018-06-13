*** Settings ***
Resource    keywords.robot

*** Variables ***
# login
${login_or_register}  id=login_link
${input_username}  id=id_login-username
${input_password}  id=id_login-password
${submit_login}  xpath=//button[contains(concat(' ', normalize-space(@class), ' '), ' log-in-tbutton')]

#--------------------------------------------------------------------------------------
#  Place Order
#--------------------------------------------------------------------------------------

# offline order  order_info
${place_order}  xpath=//a[@href='/en-gb/dashboard/orders/add/']
${purchase_at_pharmacy}  xpath=//span[@class='list-group-item-text'][contains(text(), 'Purchase at the pharmacy')]
${order_by_phone}  xpath=//span[@class='list-group-item-text'][contains(text(), 'Order by phone')]
${add_order.site}  xpath=//div[@class='Select-value']
${add_order.select_site}  xpath=//div[@class='order-site']//div[@class='Select-placeholder']
${add_order.reset_site}  xpath=//div[@id='order_info']//span[@class='Select-clear']
${add_order.site_dropdown}  xpath=//div[@class='order-site']//span[@class='Select-arrow-zone']
${add_order.choose_site}  xpath=//div[@class='Select-menu-outer']//*[contains(text(), 'vet-pharm.devel.vetopharm.quintagroup.com')]
${add_order.choose_user}  xpath=//a[contains(text(), 'Choose User')]

#offline order  choose_user
${choose_user.email_input}  id=id_email
${choose_user.search_with_filter}  xpath=//button[@name='search'][contains(text(), 'Search')]
${choose_user.email_filter_results}  //div[@class='user-search']//tbody//td[2]
${choose_user.reset_search_filter}  xpath=//div[@class='user-search']//button[contains(text(), 'Reset')]
${choose_user.first_name_input}  id=id_first_name
${choose_user.last_name_input}  id=id_last_name
${choose_user.name_filter_results}  //div[@class='user-search']//tbody//td[1]
${choose_user_btn}  xpath=//button[contains(text(), 'Choose this user')]
${choose_user.email}  xpath=//div[@id="user_choose"]/div[1]//tr[2]//td[2]

${choose_user.add_new_user}  xpath=//a[contains(text(), 'Add new User')]
${choose_user.type_of_customer}  xpath=//span[@id='select2-chosen-3']
${choose_user.type_input}  id=s2id_autogen3_search
${choose_user.individual_customer}  xpath=//div[@class='select2-result-label']

#offline order  form_basket
${form_basket}  xpath=//a[contains(text(), 'Form Basket')]
${form_basket.search_button}  xpath=//div[@class='product-list']//button[contains(text(), 'Search')]
${form_basket.reset_search_filters}  xpath=//div[@class='product-list']//button[contains(text(), 'Reset')]

${form_basket.search_by_title}  id=id_title
${form_basket.search_by_lab}  id=id_laboratoryDiff
${form_basket.search_by_CIP_code}  id=id_cip
${form_basket.search_by_UPC_code}  id=id_upc

${form_basket.by_title_result}  xpath=//div[@class='product-list']//td[1]
${form_basket.by_laboratory_results}  xpath=//div[@class='product-list']//td[2]
${form_basket.by_code_results}  xpath=//div[@class='product-list']//td[3]

${form_basket.add_available_prod}  xpath=//td[contains(text(), 'Available')]/..
${form_basket.chosen_prod_title}  .//td[1]
${form_basket.add_to_order_btn}  .//td[8]//button[contains(text(), 'Add to order')]
${form_basket.quantity_box}  .//td[8]//input[@name='quantity']

${form_basket.basket}  xpath=//div[@id='basket_choose']//div[@class='basket']//tbody
${form_basket.basket.added_prod_title}  xpath=//div[@id='basket_choose']//div[@class='basket']//tbody//td[1]
${form_basket.basket.added_quantity}  xpath=//div[@id='basket_choose']//div[@class='basket']//tbody//td[5]
${form_basket.basket.remove_product}  xpath=//div[@class='basket']//button[@class='btn btn-danger']

#offline order  shipping
${shipping}  xpath=//div[@id='placeOrderBlock']//a[contains(text(), 'Shipping')]
${shipping.input_method}  xpath=//div[@class='well form-group']//div[@class='Select-placeholder']
${shipping.select_method}  xpath=//div[@class='Select-menu-outer']//*[contains(text(), 'Pickup at the pharmacy (€0.00)')]
${shipping.select_address_pharmacy}  xpath=//div[@class='col-md-6']//address/strong[2]
${shipping.add_address}  xpath=//button[contains(text(), 'Add an address')]
${shipping.add_address_modal}  xpath=//div[@class='modal-dialog']
${shipping.autocomplete_address}  xpath=//input[@id='id_autocomplete']
${shipping.cannot_find_address_btn}  xpath=//button[contains(text(), "I can't find my address")]
${shipping.autocomplete_form_arrow}  xpath=//div[@class='address-form']//span[@class='Select-arrow-zone']
${shipping.autocomplete_submit}  xpath=//div[@class='modal-dialog']//button[contains(text(), 'Submit')]
${shipping.bill_to_address}  xpath=//button[contains(text(), 'Bill to this address')]
${shipping.added_billing_ad}  xpath=//div[@class='col-md-6'][2]//address
${shipping.ship_to_address}  xpath=//button[contains(text(), 'Ship to this address')]
${shipping.added_shipping_ad}  xpath=//div[@class='col-md-6'][1]//address
${shipping.select_title}  xpath=//span[@id='react-select-4--value']//div[@class='Select-placeholder']

${shipping.method_input}  xpath=//span[@id='react-select-3--value']//div[@class='Select-placeholder']
${shipping.selected_method}  xpath=//span[@id='react-select-3--value']//div[@class='Select-value']
${choose_from_autocomplete}  xpath=//div[@class='Select-menu-outer']/*

#offline order  payment
${payment}  xpath=//a[contains(text(), 'Payment')]
${payment.select_method}  xpath=//div[@id='orderPayment']//div[@class='Select-placeholder']
${payment.choose_credit_card}  xpath=//div[@class='Select-menu-outer']//*[contains(text(), 'Credit Card')]

#offline order  order_preview
${order_preview}  xpath=//a[contains(text(), 'Order Preview')]
${order_preview.basket_summary_incl_tax}  xpath=//td[contains(text(), 'Basket summary')]/../td[2]
${order_preview.add_discount_to_basket}  xpath=//div[@class='row'][3]//button
${order_preview.discount_type_autocomp}  xpath=//span[@id='react-select-7--value']/div[1]
${order_preview.edit_discount_type}  xpath=//span[@id='react-select-8--value']/div[1]
${order_preview.discount_input}  xpath=//label[contains(text(), 'Discount value')]/../input
${save}  xpath=//button[contains(text(), 'Save')]
${order_preview.applied_basket_discount}  xpath=//td[contains(text(), 'Basket summary')]/../../tr[2]
${order_preview.delete_discount}  xpath=//button[@class='btn btn-danger pull-right']
${order_preview.edit_discount}  xpath=//button[@class='btn btn-primary pull-right']

${order_preview.add_shipping_discount}  xpath=//div[@class='row'][6]//button
${order_preview.shipping_discount_autocomp}  xpath=//span[@id='react-select-7--value']/div[1]
${order_preview.shipping_summary_incl_tax}  xpath=//td[contains(text(), 'Shipping cost')]/../td[2]
${order_preview.order_message}  xpath=//textarea[@id='order-pharmacist-comment']
${order_preview.total_price}  xpath=//td[contains(text(), 'Order total')]/../td[3]
${order_preview.place_order}  xpath=//button[@class='btn btn-primary btn-lg'][contains(text(), 'Place Order')]
${order_preview.view_after_payment}  xpath=//a[contains(text(), 'View my order')]

${check_email.confirmation_title}  xpath=//span[contains(text(), 'ORDER NUMBER')]
${check_email.proceed_to_payment_btn}  xpath=//a[contains(text(), 'Proceed to payment')]
${check_email.vat_exempt_msg}  xpath=//div//p[contains(text(), 'YOUR ORDER IS EXEMPT FROM FRENCH VAT (VAT = 0%).')]
${check_email.proceed_to_payment}  xpath=//a[contains(text(), 'Proceed to payment')]

${delete_user}  xpath=//a[@class='btn btn-danger']
${confirm_user_deletion}  xpath=//button[@class='btn btn-danger']
${customers_list}  xpath=//i[@class='icon-group']/..

#--------------------------------------------------------------------------------------
#  Questions&Answers
#--------------------------------------------------------------------------------------

#questions&answers  ask_question

${ask_question.q&a_button}  xpath=//div[@id='main_tabs']//a[contains(text(), 'Q&A')]
${ask_question.ask_a_question_btn}  xpath=//div[@class='add_question']/button
${ask_question.send_message}  xpath=//div[@class='add_question']//button[@class='btn button_prime send-message']
${ask_question.last_question}  xpath=//div[@class='panel-body']//tbody//tr[1]

${tag.species_eng}  xpath=//ul[@class='select2-results']/li/div
${add_answer}  xpath=//div[@class='panel panel-warning']//a[@class='btn btn-warning']
${ask_question.save}  xpath=//div[@class='content']//button[@class='btn btn-primary']
${website_to_display}  xpath=//ul[@class='select2-results']//div
${chosen_website_to_diplay}  xpath=//div[@id='s2id_id_sites_to_display']//div
${approve_question}  xpath=//a[@class='btn btn-success']
${search_question}  xpath=//button[@class='btn search_button border_site_style']
${found_question_in_list}  xpath=//div[@id='product-description']/div[1]/div[1]
${view_found_question}  .//div[@class='link_icon']/a
${question_tag}  xpath=//div[@class='question_tags']//span

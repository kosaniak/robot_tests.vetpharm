import os
import sys
import uuid
from datetime import datetime
from functools import wraps
from random import choice, randint
from string import ascii_lowercase
from time import sleep
from traceback import print_exc

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import asserts

from robotpageobjects import Page, robot_alias

import sensitive_settings


class VetoPharmHomePage(Page):
    """ Models the VetoPharm home page at:
        HOST:http://veto-pharm.devel.vetopharm.quintagroup.com"""


    # Allows us to call this page
    # something other than the default "VetDoc Home Page"
    # at the end of keywords.
    name = "VetoPharm"
    TLDS = ('com net org mil edu de biz de ch at ru de tv com'
    'st br fr de nl dk ar jp eu it es com us ca pl')
    # inheritable dictionary mapping human-readable names
    # to Selenium2Library locators. You can then pass in the
    # keys to Selenium2Library actions instead of the locator
    # strings.
    selectors = {
        "login or register": "id=login_link",
        "input username": "id=id_login-username",
        "input password": "id=id_login-password",
        "register": "xpath=(//span[contains(text(),'Register')])",
        "registration email": "id=id_registration-email",
        "registration password": "id=id_registration-password1",
        "confirm password": "id=id_registration-password2",
        "login submit": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' log-in-tbutton')])",
        "registration submit": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), 'register-tbutton')])",
        "back to site": "xpath=(//i[@class='icon-home'])",
        "log out": "id=logout_link",
        "all products": "xpath=(//a[contains(text(),'All products')])",
        "list of products": "xpath=(//div[@class='row product-list'])",
        "add to basket": "xpath=(//li[contains(concat(' ', normalize-space(@class), ' '), ' my-basket-tbutton')])",
        "continue shopping after adding": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' continue-shopping-tbutton')])",
        "add product with instructions": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' add-to-basket-tbutton')])",
        "delete from basket": "xpath=(//i[contains(concat(' ', normalize-space(@class), ' '), ' remove-from-basket-tbutton')])",
        "list of wishlists": "xpath=(//li[contains(concat(' ', normalize-space(@class), ' '), ' my-wishlist-tbutton')])",
        "wishlist view": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' view-wish-list-tbutton')])",
        "product quantity": "id=id_lines-0-quantity",
        "update quantity": "id=update-wish-quantities",
        "wishlist settings": "xpath=(//i[@class='fa fa-chevron-down'])",
        "delete product": "xpath=(//a[@class='remove-from-wishlist-tbutton'])",
        "remove from wishlist": "xpath=(//button[@class='btn btn-lg btn-danger'])",
        "create new wishlist": "xpath=(//div[@class='wish_butt'])",
        "wishlist name": "id=id_name",
        "save wishlist": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' save-wishlist-tbutton')])",
        "wishlists": "xpath=(//table[@class='table table-bordered '])",
        "delete wishlist": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' confirm-remove-from-wishlist-tbutton')])",
        "health center": "xpath=(//div[@class='health_centre health-centre-nav-menu'])",
        "animals": "xpath=(//a[@href='/en-gb/health_centre/animals/'])",
        "add animal": "xpath=(//a[@href='/en-gb/health_centre/animal/create'])",
        "species": "xpath=(//span[@class='select2-arrow'])",
        "species list": "id=select2-results-1",
        "selected species": "id=select2-chosen-1",
        "breed":"xpath=(//div[@id='s2id_id_breed']//span[@class='select2-arrow'])",
        "breed list": "id=select2-results-2",
        "sex": "id=id_sex",
        "sex list": "id=select2-results-3",
        "selected breed": "id=select2-chosen-2",
        "questions list": "xpath=(//div[@class='helth-info col-sm-6'])",
        "all animals": "xpath=(//a[contains(text(),'My animals')])",
        "my prescriptions": "xpath=(//a[@href='/en-gb/health_centre/prescriptions/'])",
        "add prescription": "xpath=(//a[@class='btn add_new_button add-new-prescription-tbutton'])",
        "prescription title": "id=id_title",
        "save prescription": "id=ajax-save-prescription",
        "prescription date": "id=id_created_date",
        "calendar": "xpath=(//div[@class='datetimepicker-days'])",
        "add animals": "id=add-animals-under",
        "list of animals": "xpath=(//div[@class='animals-container container'])",
        "select animal": "id=add-animals-groups",
        "add veterinarian": "id=add-veterinarian",
        "list of vets": "xpath=(//div[@class='vet-search-results'])",
        "select veterinarian": "xpath=(//button[@class='btn btn-default link_site_style'][contains(text(),'Close')])",
        "add products": "id=add-products-under",
        "add products left": "id=add-products-left",
        "search field": "xpath=(//*[@id='data-container']/form/div/div/div/input)",
        "search products": "id=ajax-search",
        "products list": "xpath=(//div[@class='products_list'])",
        "select product": "xpath=(//*[@id='add-products']/div/div/div[3]/button)",
        "en button": "id=en-gb-comp",
        "fr button": "id=fr-comp",
        "widgets-list": "xpath=(//i[@class='fa fa-caret-down'])",
        "currency-widget": "id=currency-widget",
        "currency": "xpath=(//li[@id='currency-widget']//a[@class='trigger'])",
        "currency logo": "xpath=(//a[@class='dropdown-toggle']//i[@class='curr_logo'])",
        "selected currency": "xpath=(//div[@class='product_price']//i[@class='curr_logo'])",
        "user account": "xpath=(//div[@class='user-account'])",
        "my profile": "xpath=(//a[contains(text(),'My profile')])",
        "edit profile": "xpath=(//a[@class='btn button_color_border edit_prof_btn'])",
        "delete profile": "id=delete_profile",
        "account pasword": "id=id_password",
        "delete account": "xpath=(//button[@class='btn button_prime'])",
        "shipping country": "xpath=(//li[@id='shipping-widget']//a[contains(@class, 'trigger')])",
        "tax dropdown":  "xpath=(//ul[@class='tax_dropdown'])",
        "view prices": "xpath=(//span[contains(text(),'View prices')])",
        "search filters": "xpath=(//div[contains(text(),'FILTERS')])",
        "availability filter": "xpath=(//button[@class='filter-button']/span[contains(text(),'Availability')])",
        "availiable product": "xpath=(//span[@class='item-name'][contains(text(),'Available')])",
        "prescription filter": "xpath=(//button[@class='filter-button']/span[contains(text(),'Prescription ?')])",
        "no prescription": "xpath=(//span[@class='item-name'][contains(text(),'Issuance without prescription')])",
        "add files to prescription": "id=add-files-under",
        "add file": "xpath=(//div[@class='file-input-container'])",
        "cancel new prescription": "xpath=(//a[@href='/en-gb/health_centre/prescriptions/'][contains(text(), Cancel)])",
        "prescriptions list body": "xpath=(//*[@id='column-wrapper']/div/div[2]/div[3]/div/table/tbody)",
        "prescriptions filter button": "id=select2-chosen-1",
        "vet filter for prescriptions": "xpath=(//div[@class='select2-result-label'][contains(text(), 'Veterinarian')])",
        "animals filter for prescriptions": "xpath=(//div[@class='select2-result-label'][contains(text(), 'Animals')])",
        "groups filter for prescriptions": "xpath=(//div[@class='select2-result-label'][contains(text(), 'Group of animals')])",
        "products filter for prescriptions":"xpath=(//div[@class='select2-result-label'][contains(text(), 'Products')])",
        "prescription search field": "id=search-set-input",
        "prescription search button": "xpath=(//button[@class='btn search_button border_site_style'])",
        "found prescriptions list": "xpath=(//div[@class='list_prescription'])",
        "clear button": "id=reset-btn",
        "proceed to checkout button": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' procced-to-checkout-tbutton')])",
        "checkout guest": 'id=id_options_2',
        "continue checkout button": "xpath=(//button[@class='btn btn-lg btn-block btn-primary'][contains(text(),'Continue')])",
        "user email for checkout": "id=id_username",
        "new checkout address": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' add-new-address-tbutton')])",
        "address autocomplete for checkout": "id=id_autocomplete",
        "checkout with account": "id=id_options_0",
        "checkout company": "xpath=(//label[@for='company_2'][contains(text(), 'Quintagroup')])",
        "checkout company Quinta": "xpath=(//label[@for='company_1'][contains(text(), 'Quinta')])",
        "proceed company checkout": "xpath=(//button[@class='btn button_prime'])",
        "added checkout addresses": "xpath=(//div[@class='choose-block'])",
        "checkout address": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' ship-to-this-address-tbutton')])",
        "billing address": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' select-billing-address-tbutton')])",
        "business parcel delivery": "xpath=(.//*[@id='3']/div[1]/div/div[4]/form/button)",
        "select paypal": "xpath=(//div[@class='pay_select']//input[@value='paypal']/../button[contains(concat(' ', normalize-space(@class), ' '), ' select-tbutton')])",
        "paypal login frame": "xpath=(//iframe[@name='injectedUl'])",
        "paypal email": "xpath=(//*[@id='email'])",
        "paypal password": "xpath=(//*[@id='password'])",
        "paypal login btn": "xpath=(//*[@id='btnLogin'])",
        "paypal continue btn": "id=button",
        "place order": "id=place-order",
        "continue shopping": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' countinue-shopping-tbutton')])",
        "berlin": "xpath=(//div[@class='pac-item']/span[contains(text(), 'Europaplatz, Berlin, Germany')])",
        "continue checkout": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' address-continue-tbutton')])",
        "select paybox": "xpath=(//div[@class='pay_select']//input[@value='paybox']/../button[contains(concat(' ', normalize-space(@class), ' '), ' select-tbutton')])",
        "paybox cardnumber": "xpath=(//*[@id='id_number'])",
        "paybox ccv number": "xpath=(//*[@id='id_ccv'])",
        "continue paybox payment": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' continue-payment-tbutton')])",
        "view order status": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' view-order-status-tbutton')])",
        "checkout with a new account": 'id=id_options_1',
        "my basket": "xpath=(//li[contains(concat(' ', normalize-space(@class), ' '), ' my-basket-tbutton')])",
        "paris": "xpath=(//div[@class='pac-item']/span[contains(text(), 'France')])",
        "pick up at the pharmacy": "xpath=(//*[@id='default']/div[1]/div/div[3]/div[1]/div[1]/div[2]/div/div/div[3]/form/button)",
        "Livraison domicile (Suisse)": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' select-method-tbutton')])",
        "select bank transfer": "xpath=(//div[@class='pay_select']//input[@value='bank-transfer']/../button[contains(concat(' ', normalize-space(@class), ' '), ' select-tbutton')])",
        "received email letters": "xpath=(//*[@id='message-htmlpart1']/div/p[2]/a)",
        "paypal email login": "xpath=(//form[@name='login']//input[@id='email'])",
        "paypal password login": "xpath=(//form[@name='login']//input[@id='password'])",
        "home delivery": "xpath=(//*[@id='2']/div/div/div[3]/form/button)",
        "geneva": "xpath=(//div[@class='pac-item']/span[contains(text(), 'Switzerland')])",
        "bank cheque": "xpath=(//div[@class='pay_select']//input[@value='bank-cheque']/../button[contains(concat(' ', normalize-space(@class), ' '), ' select-tbutton')])",
        "dashboard": "xpath=(//a[contains(text(),'Dashboard')])",
        "dashboard content": "xpath=(//*[@id='default']/nav[2]/div/div[2]/ul/li[6]/a)",
        "dashboard reviews": "xpath=(//a[contains(text(),'Reviews')])",
        "dashboard prescriptions": "xpath=(//a[contains(text(),'Prescriptions')])",
        "les gets": "xpath=(//div[@class='pac-item']/span[contains(text(), 'Presnoy, France')])",
        "flex delivery service": "xpath=(//*[@id='2']/div[2]/div/div[3]/form/button)",
        "during pickup payment": "xpath=(//div[@class='pay_select']//input[@value='during-pickup']/../button[contains(concat(' ', normalize-space(@class), ' '), ' select-tbutton')])",
        "write a review button": "xpath=(//*[@id='column-wrapper']/div/div[2]/section[1]/div/div/div[3]/div/div[1]/p[2]/small/a[2])",
        "all reviews before": "xpath=(//*[@id='column-wrapper']/div/div[2]/section[1]/div/div/div[3]/div/div[1]/p[2]/small/a[1])",
        "submit a review button": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' submit-review-tbutton')])",
        "all reviews after": "xpath=(//*[@id='column-wrapper']/div/div[2]/section[1]/div/div/div[3]/div/div[1]/p[2]/small/a)",
        "filter reviews": "xpath=(//button[@class='btn btn-primary top-spacer'])",
        "rating stars box editing": "xpath=(//*[@id='edit_review_form']/div[1]/div/div[1])",
        "rating stars box": "xpath=(//*[@id='add_review_form']/fieldset/div[1]/div/div[1])",
        "total product price excl vat": "xpath=(//*[@id='basket_totals']/div[1]/ul/li[1]/span)",
        "total product price incl vat": "xpath=(//*[@id='basket_totals']/div[1]/ul/li[3]/span)",
        "add to basket from preview": "xpath=(//*[@id='add-to-basket-modal']/div/div/div[4]/a[1])",
        "unreferenced product": "xpath=(//span[@class='item-name'][contains(text(),'Unreferenced product')])",
        "unreferenced product (medicated feeds)": "xpath=(//span[@class='item-name'][contains(text(),'Unreferenced product (For the manufacture of medicated feeds)')])",
        "manufacturing suspended": "xpath=(//span[@class='item-name'][contains(text(),'Manufacturing suspended')])",
        "manufacturing stopped": "xpath=(//span[@class='item-name'][contains(text(),'Manufacturing stopped')])",
        "marketing auth suspended": "xpath=(//span[@class='item-name'][contains(text(),'Marketing authorisation suspended')])",
        "prescription required": "xpath=(//span[@class='item-name'][contains(text(),'Prescription required. Dispensing is prohibited to public')])",
        "category filter": "xpath=(//button[@class='filter-button']/span[contains(text(),'Category')])",
        "veterinary drugs": "xpath=(//span[@class='item-name'][contains(text(),'Veterinary drugs')])",
        "issuance on prescription": "xpath=(//span[@class='item-name'][contains(text(),'Issuance on prescription')])",
        "livestock health program filter": "xpath=(//button[@class='filter-button']/span[contains(text(),'Livestock Health Program (LHP)')])",
        "LHP beef production": "xpath=(//span[@class='item-name'][contains(text(),'Beef production')])",
        "out of stock filter": "xpath=(//span[@class='item-name'][contains(text(),'Unavailable (out of stock)')])",
        "drug list filter": "xpath=(//button[@class='filter-button']/span[contains(text(),'Drug list')])",
        "drug list not applicable": "xpath=(//span[@class='item-name'][contains(text(),'Not applicable')])",
        "on prescription": "xpath=(//span[@class='item-name'][contains(text(),'Issuance on prescription')])",
        "login for drug request": "xpath=(//a[@class='btn btn-primary btn-large'])",
        "my drug requests": "xpath=(//li[contains(concat(' ', normalize-space(@class), ' '), ' my-drug-requests-tbutton')])",
        "add prescr to drug request": "xpath=(//button[@class='btn btn-default button_site_style'][contains(text(), 'OK')])",
        "dashboard health of animals": "xpath=(//*[@id='default']/nav[2]/div/div[2]/ul/li[12])",
        "dashboard drug requests": "xpath=(//a[contains(text(),'Drug Requests')])",
        "edit prod drug request": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' edit-product-line-tbutton')])",
        "list of drug requests": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' nav-my-drug-requests-tbutton')])",
        "OK btn for prescr in request": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' ok-close-prescr-search-tbutton')])",
        "edit drug request": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' edit-request-tbutton')])",
        "drug request link": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' request-detail-tbutton')])",
        "drug request comments": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' pharmacist-comment-tbutton')])",
        "select all prods in drug request": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' select-all-products-tbutton')])",
        "my basket from request": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' request-my-basket-tbutton')])",
        "update quantity in basket": "xpath=(//a[contains(concat(' ', normalize-space(@class), ' '), ' update-quantity-tbutton')])",
        "proceed in checkout": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' proceed-tbutton')])",
        "home delivery items": "xpath=(//div[@class='shipp_item']//i)",
        "home delivery(Ger, Bel, Lux)": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' select-method-tbutton')])",
        "approve drug request": "xpath=(//div[contains(text(),'Approved')])",
        "reject drug request": "xpath=(//div[contains(text(),'Rejected')])",
        "delete prescription at dashboard": "xpath=(//a[@class='btn btn-danger'])",
        "delete prescription": "xpath=(//button[@class='btn btn-danger'])",
        "delete drug request": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' delete-request-tbutton')])",
        "confirm delete drug request": "xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' confirm-delete-request-tbutton')])"
    }

    def account_cleanup(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            self = args[0]
            try:
                return fn(*args, **kwargs)
            except Exception as outer_e:
                raise outer_e
            finally:
                try:
                    self.delete_account(sensitive_settings.register_password)
                except Exception:
                    print(print_exc(sys.exc_info()))
                    print('\nThe above exception occurred during handling the following exception:\n')
                    raise outer_e
        return wrapper

    def gen_name(self, length):
        """Generate a random name with the given number of characters."""
        return ''.join(choice(ascii_lowercase) for _ in xrange(length))

    def email_generator(self):
        """Generate fake e-mail addresses."""
        user = self.gen_name(randint(3, 10))
        host = self.gen_name(randint(4, 20))
        return '%s@%s.%s' % (user, host, choice(self.TLDS.split()))

    def gen_password(self):
        password= uuid.uuid4().hex
        return password

    @robot_alias("maximize__window")
    def maximize_browser_window(self):
        self._current_browser().maximize_window()
        return self

    def close_prev_window_tab(self):
        handles = self._current_browser().get_window_handles()
        self.select_window(handles[0])
        self.close_window()
        self.select_window()
        return self

    @robot_alias("Login__into__user__account")
    def successful_login(self):
        self.login_into_acc(sensitive_settings.email, sensitive_settings.password)
        self.body_should_contain_text('Welcome back', 
            'Login failed for user')
        return self

    @robot_alias("Try__to__login__with__incorrect__credentials")
    def unsuccessful_login(self):
        self.login_into_acc(self.email_generator(), self.gen_password())
        self.body_should_contain_text('Please enter a correct username and password. Note that both fields may be case-sensitive', 
            'No alert message about incorrect credentials')
        return self

    def login_into_acc(self, email, password):
        self.click_element("login or register")
        self.type_in_box(email, "input username")
        self.type_in_box(password, "input password")
        self.click_button("login submit")
        sleep(4)
        return self

    @robot_alias("Logout__from__account")
    def log_out(self):
        self.click_element("user account")
        self.click_element("log out")
        self.body_should_contain_text('Login or register',
            'Logout failed')
        return self

    @robot_alias("Return__to__site")
    def back_to_website(self):
        self.click_element("back to site")
        self.body_should_contain_text('All products', 'Return to site button does not work')
        return self

    @robot_alias("Try__to__register__already__taken__email")
    def taken_email_registration(self):
        self.register_account(sensitive_settings.email, sensitive_settings.password)
        self.body_should_contain_text('A user with that email address already exists', 
            'Successful registration for already taken email')
        return self

    @robot_alias("Try__to__register__the __invalid__email")
    def invalid_email_registration(self):
        self.register_account(self.email_generator()[:-5], self.gen_password())
        self.body_should_contain_text('Enter a valid email address',
            'Successful registration for invalid email address')
        return self

    @robot_alias("Use__too__short__password")
    def invalid_password_registration(self):
        self.register_account(self.email_generator(), self.gen_password()[:3])
        self.body_should_contain_text('Ensure this value has at least 6 characters (it has',
            'No alert message about insecure password')
        return self

    @robot_alias("Unsuccessful__password__confirmation")
    def wrong_password_confirmation(self):
        self.click_element("login or register")
        self.click_element("register")
        sleep(2)
        self.type_in_box(self.email_generator(), "registration email")
        self.type_in_box(self.gen_password(), "registration password")
        self.type_in_box(self.gen_password(), "confirm password")
        self.click_button("registration submit")
        self.body_should_contain_text('The two password fields didn\'t match.',
            'No alert message about password confirmation fail')
        return self

    def register_account(self, email=None, password=None):
        if email == None:
            email = self.email_generator()
            password = self.gen_password()
        elif email == sensitive_settings.register_email:
            password = sensitive_settings.register_password
        self.click_element("login or register")
        self.click_element("register")
        sleep(2)
        self.type_in_box(email, "registration email")
        self.type_in_box(password, "registration password")
        self.type_in_box(password, "confirm password")
        self.click_button("registration submit")
        sleep(8)
        self.capture_page_screenshot()
        if self._page_contains('To activate your account, please click the link sent to your mailbox'):
            self.activate_new_account(email, password)
            self.wait_until_element_is_visible("id=header-middle", 30)
            self.body_should_contain_text('Your account was confirmed successfully',
                'The account was not activated')
        return password

    def activate_new_account(self, email, password):
        self._current_browser().get('https://mail29.lwspanel.com/webmail/')
        if self._is_element_present("id=rcmloginuser"):
            self.type_in_box(email, "id=rcmloginuser")
            self.type_in_box(password, "id=rcmloginpwd")
            self.click_element("id=rcmloginsubmit")
        all_letters = self.find_activation_letter()
        while all_letters == []:
            self.reload_page()
            all_letters = self.find_activation_letter()
        self.click_element(all_letters[0])
        sleep(3)
        while self._page_contains("Thank you for registering on VetPharm!") is not True:
            self.reload_page()
            all_letters = self.find_activation_letter()
            self.click_element(all_letters[0])
        self.select_frame("id=messagecontframe")
        self.focus("received email letters")
        self.click_element("received email letters")
        sleep(3)
        self.close_prev_window_tab()
        return self

    def find_activation_letter(self):
        self.wait_until_element_is_enabled("id=mailview-top", 25)
        body = self.find_element("id=mailview-top")
        all_letters = body.find_elements_by_xpath("//td[@class='subject']")
        return all_letters

    @robot_alias("Delete__profile")
    def delete_account(self, password):
        self.click_element("user account")
        self.click_element("my profile")
        self.mouse_over_element_in_viewport("edit profile")
        self.click_element("edit profile")
        self.wait_until_element_is_visible("delete profile", 15)
        self.mouse_over_element_in_viewport("delete profile")
        self.click_element("delete profile")
        self.wait_until_element_is_visible("account pasword")
        self.type_in_box(password, "account pasword")
        self.click_element("delete account")
        self.body_should_contain_text("Your profile has now been deleted. Thanks for using the site", "Profile was not deleted")
        return self    

    def type_in_box(self, txt, search_box):
        logger.info("Typing text '%s' into text field '%s'." % (txt, search_box))
        for letter in txt:
            self.find_element(search_box).send_keys(letter)
            sleep(0.25)
        return self
        
    def body_should_contain_text(self, str, error_message, ignore_case=True):
        result_msg = str.lower() if ignore_case else str
        result_msg = result_msg.encode("utf-8")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_true(result_msg in body_txt, error_message)
        return self

    @robot_alias("switch__between__languages")
    def change_language(self):
        self.click_element("fr button")
        self.body_should_contain_text("Tous les produits", "French was not selected")
        self.click_element("en button")
        self.body_should_contain_text("All products", "English was not selected")
        return self

    @robot_alias("select__currency")
    def change_currency(self):
        self.select_with_search_filters()
        self.click_element("widgets-list")
        self.click_element("currency-widget")
        currency_widget = self.find_element("currency-widget")
        currency_list = currency_widget.find_elements_by_tag_name("li")
        currency = choice(currency_list)
        selected_currency = self.get_text(currency)
        self.click_element(currency)
        self.click_element("widgets-list")
        self.element_text_should_be("currency", selected_currency)
        currency_logo = self.get_text("currency logo")
        prod_curr_list = self.find_elements("selected currency")
        self.mouse_over_element_in_viewport(prod_curr_list[1])
        self.element_text_should_be("selected currency", currency_logo)
        return self

    @robot_alias("select__shipping__country")
    def select_country(self):
        self.click_element("shipping-widget")
        shipping_widget = self.find_element("shipping-widget")
        counrty_list = shipping_widget.find_elements_by_tag_name("li")
        selected_country = choice(counrty_list)
        country = self.get_text(selected_country)
        self.click_element(selected_country)
        self.click_element("widgets-list")
        self.element_text_should_be("shipping country", country)
        return self

    @robot_alias("select__prices__view")
    def view_prices(self):
        self.click_element("view prices")
        tax_dropdown = self.find_element("tax dropdown")
        tax_list = tax_dropdown.find_elements_by_tag_name("li")
        selected_tax = choice(tax_list)
        price_view = self.get_text(selected_tax).lower()
        self.click_element(selected_tax)
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('no prescription')
        product = self.select_product()
        tax = product.find_element_by_tag_name("sup")
        asserts.assert_true(self.get_text(tax).lower() in price_view, 
            'Price view does not include tax information')
        return self

    @robot_alias("Add__product__to__wishlist__from__listing")
    def add_to_wishlist_from_listing(self):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('no prescription')
        product = self.select_product()
        self.mouse_over_element_in_viewport(product)
        wishlist = product.find_element_by_xpath('.//i')
        default_wishlist = product.find_elements_by_xpath('.//label')
        pr_name = self.product_name(product)
        print pr_name
        self.mouse_over_element_in_viewport(wishlist)
        self.click_element_at_coordinates(wishlist, 0, 0)
        sleep(2)
        self.click_element_at_coordinates(default_wishlist[0], 0, 0)
        self.mouse_over_element_in_viewport("list of wishlists")
        self.click_element_at_coordinates("list of wishlists", 0, 0)
        self.click_element("wishlist view")
        sleep(4)
        self.body_should_contain_text(pr_name, 'Selected product was not added to wishlist')
        return self

    @robot_alias("Add__product__to__wishlist__from__product__page")
    def add_to_wishlist_from_product_page(self):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('no prescription')
        pr_name = self.product_preview_page()
        print pr_name
        self.click_element("xpath=(//div[@class='wishlist_butt'])")
        self.click_element("xpath=(//label[@class='link_site_style'])")
        sleep(1)
        self.mouse_over_element_in_viewport("list of wishlists")
        self.click_element_at_coordinates("list of wishlists", 0, 0)
        self.click_element("wishlist view")
        sleep(4)
        self.body_should_contain_text(pr_name, 'Selected product was not added to wishlist')
        return self

    @robot_alias("Add__product__to__wishlist__from__recently__viewed")
    def add_to_wishlist_from_recently_viewed(self):
        for i in range(4):
            self.click_element("all products")
            self.select_with_search_filters()
            self.select_with_prescription_filter('no prescription')
            self.product_preview_page()
        recently_viewed = self.find_elements("xpath=(//div[@class='owl-item active'])")
        choose_prod = choice(recently_viewed)
        self.mouse_over_element_in_viewport(choose_prod)
        wishlist = choose_prod.find_element_by_xpath('.//i')
        default_wishlist = choose_prod.find_elements_by_xpath('.//label')
        pr_name = self.product_name(choose_prod)
        sleep(2)
        self.mouse_over_element_in_viewport(wishlist)
        self.click_element_at_coordinates(wishlist, 0, 0)
        sleep(2)
        self.click_element_at_coordinates(default_wishlist[0], 0, 0)
        self.mouse_over_element_in_viewport("list of wishlists")
        self.click_element_at_coordinates("list of wishlists", 0, 0)
        self.click_element("wishlist view")
        sleep(4)
        self.body_should_contain_text(pr_name, 'Selected product was not added to wishlist')
        return self

    @robot_alias("Update__quantity__in__whishlist")
    def update_quantity(self):
        self.find_element("product quantity")
        self.input_text("product quantity", '3')
        self.click_element("update quantity")
        box_value = self.find_element("product quantity").get_attribute('value')
        asserts.assert_true(box_value == '3',
            "The product quantity was not updated")
        return  self

    @robot_alias("Delete__product__from__wishlist")
    def delete_wishlist_product(self):
        self.click_element("wishlist settings")
        sleep(1)
        self.click_element("delete product")
        sleep(1)
        self.click_element("remove from wishlist")
        self.body_should_contain_text('was removed from your \'Default\' wish list', 'Selected product was not removed from the wishlist')
        return self

    @robot_alias("Create_new_wishlist")
    def create_wishlist(self):
        self.click_element("list of wishlists")
        self.click_element("create new wishlist")
        self.input_text("wishlist name", 'For my cat')
        self.click_element("save wishlist")
        self.body_should_contain_text('Your wishlist has been created', 'Wishlist was not created')
        self.click_element("list of wishlists")
        self.body_should_contain_text('For my cat', 'Wishlist was not created')
        return self

    @robot_alias("Delete__the__wishlist")
    def delete_wishlist(self):
        wishlists = self.find_element("wishlists")
        last_wishlist = wishlists.find_elements_by_tag_name('td')[-1]
        dropdown_toggle = last_wishlist.find_element_by_tag_name("button")
        self.click_element(dropdown_toggle)
        delete_btn = last_wishlist.find_elements_by_tag_name("li")[-1]
        self.click_element(delete_btn)
        self.click_element("delete wishlist")
        self.body_should_contain_text("Your 'For my cat' wish list has been deleted", '')
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_false('For my cat' in body_txt, 'Wishlist was not created')
        return self

    @robot_alias("Add__product__to__basket")
    def add_to_basket_from_listing(self):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('no prescription')
        product = self.select_product()
        pr_name = self.product_name(product)
        print pr_name
        self.mouse_over_element_in_viewport(product)
        add_to_basket = product.find_element_by_xpath(".//div[@class='product-control-button']")
        sleep(2)
        self.click_element_at_coordinates(add_to_basket, 0, 0)
        sleep(2)
        self.check_veterinary_drug_label()
        sleep(5)
        self.mouse_over_element_in_viewport("add to basket")
        self.click_element_at_coordinates("add to basket", 0, 0)
        self.body_should_contain_text(pr_name, 'Selected product was not added to basket')
        return self

    @robot_alias("Add__product__to__basket__from__preview")
    def add_to_basket_from_preview(self, quantity=None):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('no prescription')
        pr_name = self.product_preview_page()
        if quantity:
            quantity_box = self.find_elements("xpath=(//input[@id='id_quantity'])")
            self.input_text(quantity_box[0], quantity)
        self.mouse_over_element_in_viewport("xpath=(//*[@id='add_to_basket_form_main']/button)")
        self.wait_until_element_is_visible("xpath=(//*[@id='add_to_basket_form_main']/button)")
        self.click_element_at_coordinates("xpath=(//*[@id='add_to_basket_form_main']/button)", 0, 0)
        sleep(4)
        self.check_veterinary_drug_label()
        sleep(5)
        self.mouse_over_element_in_viewport("add to basket")
        self.click_element_at_coordinates("add to basket", 0, 0)
        self.body_should_contain_text(pr_name, 'Selected product was not added to basket')
        return self

    @robot_alias("Add__product__to__basket__from__recently__viewed__products")
    def add_to_basket_from_recently_viewed(self, quantity=None):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('no prescription')
        pr_name = self.product_preview_page()
        print pr_name
        recently_viewed = self.find_elements("xpath=(//div[@class='owl-item active'])")
        choose_prod = choice(recently_viewed)
        self.mouse_over_element_in_viewport(choose_prod)
        add_to_basket = choose_prod.find_element_by_xpath(".//button[contains(concat(' ', normalize-space(@class), ' '), ' add-to-basket-tbutton')]")
        self.mouse_over_element_in_viewport(add_to_basket)
        self.click_element_at_coordinates(add_to_basket, 0, 0)
        sleep(4)
        self.check_veterinary_drug_label()
        sleep(3)
        self._current_browser().back()
        self.click_element("my basket")
        return self

    def check_veterinary_drug_label(self):
        self.wait_until_element_is_visible("id=add-to-basket-modal", 20)
        checkbox = self.find_elements("id=id_read_instructions", False)
        if len(checkbox) != 0 and checkbox[-1].is_displayed() != False:
                self.click_element_at_coordinates(checkbox[-1], 0, 0)
                sleep(1)
                add_to_basket = self.find_elements("add product with instructions")
                self.click_element(add_to_basket[-1])
        else:
            continue_shopping = self.find_elements("continue shopping after adding")
            self.click_element_at_coordinates(continue_shopping[-1], 0, 0)
        return self

    def product_preview_page(self, no_LHP_label=None):
        product = self.select_product(no_LHP_label=no_LHP_label)
        pr_name = self.product_name(product)
        link = product.find_element_by_xpath(".//a[@class='product_link']/div")
        self.wait_until_element_is_enabled(link, 25)
        self.mouse_over_element_in_viewport(link)
        self.click_element_at_coordinates(link, 0, 0)
        sleep(2)
        return pr_name

    def select_product(self, no_LHP_label=None):
        products_list = self.find_element("list of products")
        products = products_list.find_elements_by_tag_name("article")
        if no_LHP_label:
            products_without_LHP = [prod for prod in products if prod.find_elements_by_xpath(".//span[@class='bilan-sanitaire LHP availability-label']") == []]
            product = choice(products_without_LHP)
        else:
            product = choice(products)
        return product

    def select_with_search_filters(self):
        self.wait_until_element_is_visible("search filters")
        self.click_element("search filters")
        self.click_element("availability filter")
        self.click_element("availiable product")
        sleep(1)
        return self

    def select_with_prescription_filter(self, prescription_type):
        self.click_element("search filters")
        self.click_element("prescription filter")
        sleep(2)
        self.click_element(prescription_type)
        return self

    def select_with_LHP_filter(self):
        self.click_element("search filters")
        self.click_element("livestock health program filter")
        self.click_element("LHP beef production")
        sleep(1)
        return self

    def product_name(self, product_locator):
        pr_name = product_locator.find_element_by_tag_name('h3')
        product_name = self.get_text(pr_name)
        return product_name

    @robot_alias("Remove__product__from__basket")
    def delete_product(self):
        self.click_element("delete from basket")
        sleep(5)
        self.body_should_contain_text('Your basket is empty.', 'Selected product was not deleted from basket')
        return self

    @robot_alias("Write_a_review_and_evaluate_product")
    def write_product_review(self):
        self.click_element("all products")
        self.select_with_search_filters()
        pr_name = self.product_preview_page()
        while self._is_element_present("write a review button") != True:
            self.click_element("all products")
            self.select_with_search_filters()
            pr_name = self.product_preview_page()
        reviews = self.find_element("all reviews before")
        reviews_before = self.get_text(reviews)
        self.click_element("write a review button")
        self.product_rating()
        self.input_text('id=id_name_to_display', sensitive_settings.register_email)
        review_input = self.find_element("xpath=(//textarea[@id='id_body'])")
        self.input_text(review_input, 'I have used this drug')
        self.click_element("submit a review button")
        sleep(5)
        reviews_after = self.get_text("all reviews after")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_not_equal(reviews_before, reviews_after, "Review has been not submitted")
        asserts.assert_false('Write a review' in body_txt, "Review has been not submitted")
        self.page_should_contain('Thank you for reviewing this product', 'Review has been not submitted')
        self.page_should_contain_element('id=edit_review', 'It is not possible to edit a review')
        return self

    @robot_alias("Edit_a_review")
    def edit_review(self):
        self.focus('id=edit_review')
        self.click_element('id=edit_review')
        star = self.find_element("xpath=(//*[@id='edit_review_form']/div[1]/div/input)")
        prev_rate = star.get_attribute('value')
        sleep(3)
        updated_rate = self.product_rating(True)
        new_rate = updated_rate.get_attribute('value')
        if prev_rate == new_rate:
            updated_rate = self.product_rating()
            new_rate = updated_rate.get_attribute('value')
        asserts.assert_not_equal(prev_rate, new_rate, "Rating has been not changed")
        review_input = self.find_elements("xpath=(//textarea[@id='id_body'])")
        self.input_text(review_input[1], 'Great!')
        sleep(2)
        self.click_element("xpath=(//button[contains(text(),'Save your review')])")
        sleep(2)
        self.verify_successful_editing()
        return self

    @robot_alias("Delete_a_review")
    def delete_review(self):
        self.click_element('user account')
        self.click_element('dashboard')
        self.click_element('dashboard content')
        self.click_element('dashboard reviews')
        self.input_text('id=id_name', 'john')
        self.click_element("filter reviews")
        sleep(3)
        self.click_element("xpath=(//button[@class='btn btn-default dropdown-toggle'])")
        self.click_element("xpath=(//a[contains(text(),'Delete')])")
        sleep(1)
        self.click_element("xpath=(//button[@class='btn btn-danger'])")
        sleep(1)
        self.back_to_website()
        return self

    def verify_successful_editing(self):
        self.mouse_over_element_in_viewport("xpath=(//*[@id='product-reviews']/div/h2)")
        self.click_element_at_coordinates("xpath=(//*[@id='product-reviews']/div/h2)", 0, 0)
        sleep(2)
        self.find_element('id=product-reviews')
        all_reviews = self.get_text('id=product-reviews')
        asserts.assert_true('Great!' in all_reviews, "The review has not been edited")
        return self

    def product_rating(self, edit=None):
        if edit == True:
            star_box = self.find_element("rating stars box editing")
        else:
            star_box = self.find_element("rating stars box")
        stars = star_box.find_elements_by_tag_name('i')
        print stars
        prod_star = choice(stars)
        print prod_star
        self.mouse_over_element_in_viewport(prod_star)
        sleep(3)
        self.wait_until_element_is_visible(prod_star)
        self.click_element(prod_star)
        return prod_star

    @robot_alias("Add__an__animal")
    def add_animal(self):
        self.click_element("health center")
        self.click_element("animals")
        self.click_element("add animal")
        self.type_in_box('Ivanka', 'id=id_name')
        self.select_from_dropdown("species", "species list", "selected species")
        self.select_from_dropdown("breed", "breed list", "selected breed")
        self.type_in_box('20',"id=id_weight")
        self.specify_invalid_date()
        self.type_date_of_birth(str(datetime.now().day),
            str(datetime.now().month),
            str(datetime.now().year))
        self.type_in_box(self.gen_password(), "id=id_identification_number")
        self.select_from_dropdown("sex", "sex list", "id=select2-chosen-3")
        self.answer_questions()
        self.click_button("id=save-button")
        self.click_element("all animals")
        sleep(4)
        self.body_should_contain_text('Ivanka', 'The animal was not added')
        return self

    @robot_alias("Create__a__group")
    def create_group(self):
        self.click_element("xpath=(//a[contains(text(),'My groups')])")
        self.click_element("xpath=(//a[@class='btn btn-lg btn-info add-group-button button_site_style'])")
        self.type_in_box('Quintagroup', 'id=id_name')
        self.click_element("id=s2id_id_species")
        for element in self.find_element("xpath=(//input[@class='select2-input select2-focused])"):
            self.type_in_box('12', "id=id_number_of_animals")
            self.click_element("xpath=(//i[@class='fa fa-plus'])")
        animal_block = self.find_element("xpath=(//div[@class='animals-container container'])")
        list_of_animals = animal_block.find_elements_by_tag_name("img")
        animal= choice(list_of_animals)
        self.click_element(animal)
        self.click_element("xpath=(//div[@class='modal-header'])//i[@class='fa fa-times']")
        self.click_element("id=save-button")
        sleep(4)
        self.body_should_contain_text('Quintagroup', 'The group was not created')
        return self

    @robot_alias("Delete__the__group")
    def delete_group(self):
        self.click_element("xpath=(//a[contains(text(),'Quintagroup')])")
        self.click_element("xpath=(//div[@class='delete-group']//i[@class='fa fa-times'])")
        self.is_visible("xpath=(//button[@class='btn btn-danger'])")
        self.click_element("xpath=(//button[@class='btn btn-danger'])")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_false('quintagroup' in body_txt, 'The group was not deleted')
        return self


    @robot_alias("Delete__the__animal")
    def delete_animal(self):
        self.click_element("xpath=(//span[contains(text(),'Ivanka')])")
        self.click_element("xpath=(//*[@id='profile']/div/div/a)")
        sleep(5)
        self.is_visible("xpath=(//button[@class='btn btn-danger'])")
        self.click_element("xpath=(//button[@class='btn btn-danger'])")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_false('ivanka' in body_txt, 'The animal was not deleted')
        return self

    @robot_alias("Add__the__prescription")
    def add_prescription(self, product_name=None):
        self.click_element("health center")
        self.click_element("my prescriptions")
        self.click_element("add prescription")
        self.fill_in_prescription_form("prescription date", "calendar", ".//td[@class='day']")
        self.fill_in_prescription_form("add animals", "list of animals", ".//div[@class='col-sm-3 col-xs-4 animal-block']", "select animal")
        self.fill_in_prescription_form("add veterinarian", "list of vets", ".//li", "select veterinarian")
        self.mouse_over_element_in_viewport("add products")
        self.click_element_at_coordinates("add products", 0, 0)
        search_pr = self.find_element("search field")
        sleep(3)
        if isinstance(product_name, list):
            self.add_multiple_product_prescription(product_name)
        else:
            print product_name
            self.input_text(search_pr, product_name.lower().split()[0])
            self.fill_in_prescription_form("search products","products list", ".//*[@class='product']", "select product", product_name)
        self.mouse_over_element_in_viewport("save prescription")
        self.click_element_at_coordinates("save prescription", 0, 0)
        sleep(5)
        self.body_should_contain_text('A scan or photo of your prescription is required', 
            'Prescription was created without attached photo')
        self.click_element("xpath=(//*[@id='add-files-under']/i)")
        sleep(1)
        file_path = os.path.join(os.path.dirname(__file__), 'unicorn.jpg')
        self.choose_file("xpath=(//*[@id='files-contaier']/div/input[@id='file-1'])", file_path)
        sleep(2)
        self.mouse_over_element_in_viewport("save prescription")
        self.click_element_at_coordinates("save prescription", 0, 0)
        sleep(5)
        return self

    def add_multiple_product_prescription(self, products_list):
        self.search_product(products_list[0])
        for item in products_list[1:]:
                self.mouse_over_element_in_viewport("add products left")
                self.click_element_at_coordinates("add products left", 0, 0)
                self.search_product(item)
        return self

    def search_product(self, item):
        sleep(4)
        self.wait_until_element_is_visible("search field")
        self.input_text("search field", item.lower().split()[0])
        self.fill_in_prescription_form("search products","products list", ".//*[@class='product']", "select product", item)
        sleep(2)
        return self

    def check_pages(self, add_btn, list_of_items, product_name):
        for i in list_of_items:
            self.mouse_over_element_in_viewport(i)
            txt = self.get_text(i)
            if txt.lower() == product_name.lower():
                item = i.find_element_by_tag_name('i')
                break
        else:
            next_page = self.find_elements("xpath=(//li[@class='next'])")
            self.click_element(next_page[-1])
            item = self.check_pages(add_btn, list_of_items, product_name)
        return item

    def fill_in_prescription_form(self, add_btn, items, param, close_btn=None, product_name=None):
        self.wait_until_element_is_visible(add_btn)
        self.click_element(add_btn)
        sleep(5)
        if add_btn == "prescription date":
            prev_month = self.find_elements("xpath=(//th[@class='prev'])")
            self.click_element(prev_month[2])
            sleep(1)
        info_block = self.find_elements(items)
        list_of_items = info_block[0].find_elements_by_xpath(param)
        if add_btn == "search products":
            item = self.check_pages(add_btn, list_of_items, product_name)
        elif add_btn == "add veterinarian":
            elem = choice(list_of_items)
            item = elem.find_element_by_xpath(".//a[@class='btn bgc_site_style pull-right add-vet-btn']")
        elif add_btn == "prescription date":
            possible_dates = list_of_items[0:21]
            item = choice(possible_dates)
        else:
            item = choice(list_of_items)
        self.mouse_over_element_in_viewport(item)
        txt = self.get_text(item)
        print txt
        self.wait_until_element_is_visible(item)
        self.click_element(item)
        sleep(2)
        if close_btn is not None:
            self.click_element(close_btn)
            sleep(2)
            self.body_should_contain_text(self.get_text(item),
            'Required information was not added to prescription')
        sleep(3)
        return self

    def specify_invalid_date(self):
        self.date_validation('32',str(datetime.now().month), str(datetime.now().year))
        self.date_validation(str(datetime.now().day), '13', str(datetime.now().year))
        self.date_validation(str(datetime.now().day), str(datetime.now().month), '3954')
        return self 


    def date_validation(self, day, month, year):
        self.type_date_of_birth(day, month, year)
        self.click_button("id=save-button")
        self.body_should_contain_text('Date is incorrect! Example: 01/01/2017', 'dfs')
        return self

    def type_date_of_birth(self, day, month, year):
        self.type_in_box(day,"id=id_date_of_birth")
        self.type_in_box(month, "id=birth-month")
        self.type_in_box(year,"id=birth-year")
        return self

    def select_from_dropdown(self, menu_arrow, dropdown_variants, field):
        self.click_element(menu_arrow)
        dropdown_menu = self.find_element(dropdown_variants)
        element = dropdown_menu.find_elements_by_tag_name("li")
        selected_element = choice(element)
        a = self.get_text(selected_element)
        self.click_element(selected_element)
        asserts.assert_true(a in self.get_text(field), 'Value was not selected')
        return self

    def answer_questions(self):
        questions_list = self.find_element("questions list")
        questions = questions_list.find_elements_by_tag_name("div")
        for question in questions[1:5]:
            answer = question.find_elements_by_tag_name("label")
            self.click_element(choice(answer))
        return self

    @robot_alias("Redirect_to_purchase_from_bovi-pharm")
    def redirect_from_bovi_pharm(self):
        self._current_browser().get('https://bovi-pharm.devel.vetopharm.quintagroup.com/en-gb/')
        self.wait_until_element_is_visible("search filters")
        self.click_element("search filters")
        self.click_element("drug list filter")
        self.click_element("drug list not applicable")
        sleep(2)
        products_list = self.find_element("list of products")
        products = products_list.find_elements_by_tag_name("article")
        prod = choice(products)
        pr_name = self.product_name(prod)
        print pr_name
        self.mouse_over_element_in_viewport(prod)
        link = prod.find_element_by_class_name('product_link')
        self.wait_until_element_is_enabled(link)
        self.click_element(link)
        sleep(1)
        name = self.find_element("xpath=(//div[@class='descktop-product-header']/h1)")
        pr_name = self.get_text(name)
        redirect = self.find_element("xpath=(//i[@class='fa fa-external-link'])")
        self.mouse_over_element_in_viewport(redirect)
        self.wait_until_element_is_visible(redirect, 25)
        self.click_element(redirect)
        sleep(7)
        self.close_prev_window_tab()
        self.wait_until_element_is_enabled("xpath=(//div[@class='wishlist_butt'])")
        self.click_element("xpath=(//div[@class='wishlist_butt'])")
        self.click_element("xpath=(//label[@class='link_site_style'])")
        sleep(1)
        self.find_element("list of wishlists")
        self.click_element("list of wishlists")
        self.click_element("wishlist view")
        self.body_should_contain_text(pr_name, 'Selected product was not added to wishlist')
        return self

    def choose_checkout_user(self, checkout_role, email=None, password=None):
        self.click_element("proceed to checkout button")
        self.click_element(checkout_role)
        if checkout_role == "checkout with account":
            self.type_in_box(sensitive_settings.email,"user email for checkout")
            self.type_in_box(sensitive_settings.password,"account pasword")
        else:
            self.type_in_box(sensitive_settings.register_email,"user email for checkout")
        self.click_element("continue checkout button")
        return self

    def add_checkout_address(self, names=None, city=None):
        self.wait_until_element_is_visible("new checkout address", 20)
        self.mouse_over_element_in_viewport("new checkout address")
        self.click_element_at_coordinates("new checkout address", 0, 0)
        self.wait_until_element_is_visible("address autocomplete for checkout")
        self.click_element("address autocomplete for checkout")
        self.type_in_box(city,"address autocomplete for checkout")
        sleep(3)
        if not self._is_visible(city):
            self.click_element("address autocomplete for checkout")
        self.wait_until_element_is_visible(city)
        self.click_element_at_coordinates(city, 0, 0)
        if city == 'geneva':
            self.wait_until_element_is_visible("id=id_line1")
            self.type_in_box('Place Dorciere',"id=id_line1")
            self.type_in_box('1201',"id=id_postcode")
        elif city == 'les gets':
            self.wait_until_element_is_visible("id=id_line1")
            self.type_in_box('Rue du Ctre',"id=id_line1")
        elif city == 'paris':
            self.wait_until_element_is_visible("id=id_line1")
            self.type_in_box('Avenue Anatole',"id=id_line1")
            self.mouse_over_element_in_viewport("id=id_postcode")
            self.type_in_box('75007',"id=id_postcode")
        if names == True:
            self.mouse_over_element_in_viewport("id=id_first_name")
            self.type_in_box(self.gen_name(6),"id=id_first_name")
            self.type_in_box(self.gen_name(10),"id=id_last_name")
        sleep(1)
        self.mouse_over_element_in_viewport("continue checkout")
        self.click_element_at_coordinates("continue checkout", 0, 0)
        return self

    @robot_alias("Checkout_as_guest_with_payment_during_pickup")
    def checkout_as_guest_pickup_payment(self):
        self.choose_checkout_user("checkout guest")
        self.add_checkout_address(names=True, city='les gets')
        self.wait_until_element_is_visible("xpath=(//h2[contains(text(), 'Select your billing address')])")
        self.add_checkout_address(city='les gets')
        self.wait_until_element_is_visible("flex delivery service")
        self.click_element("flex delivery service")
        self.click_element("during pickup payment")
        self.test_checkout_preview()
        self.mouse_over_element_in_viewport("place order")
        self.click_element("place order")
        self.wait_until_element_is_visible("continue shopping")
        self.click_element("continue shopping")
        return self


    @robot_alias("Proceed_to_checkout_and_create_account")
    @account_cleanup
    def checkout_and_create_account(self):
        self.choose_checkout_user("checkout with a new account")
        self.current_frame_contains('Create your account and then you will be redirected back to the checkout process')
        self.register_account(sensitive_settings.register_email)
        self.mouse_over_element_in_viewport("my basket")
        self.click_element("my basket")
        self.click_element("proceed to checkout button")
        self.add_checkout_address(names=True, city='paris')
        self.wait_until_element_is_visible("xpath=(//h2[contains(text(), 'Select your billing address')])")
        self.add_checkout_address(city='paris')
        self.wait_until_element_is_visible("pick up at the pharmacy")
        self.click_element("pick up at the pharmacy")
        self.click_element("select bank transfer")
        self.test_checkout_preview()
        self.mouse_over_element_in_viewport("place order")
        self.click_element("place order")
        self.wait_until_element_is_visible("continue shopping")
        self.click_element("continue shopping")
        return self


    @robot_alias("Proceed_to_checkout_as_logged_in_user")
    def checkout_as_logged_in_user(self):
        self.choose_checkout_user("checkout with account")
        self.click_element("checkout company")
        self.click_element("proceed company checkout")
        self.click_element("checkout address")
        self.click_element("billing address")
        self.click_element("business parcel delivery")
        self.mouse_over_element_in_viewport("select paypal")
        self.click_element("select paypal")
        sleep(30)
        username = self.get_webelements("paypal email login")[0]
        self.input_text(username, 'pharmacyshoptest-buyer@gmail.com')
        password = self.get_webelements("paypal password login")[0]
        self.input_text(password, 'X4ttLgRtAj61')
        sleep(2)
        self.click_element("paypal login btn")
        sleep(10)
        self.wait_until_element_is_enabled("paypal continue btn", 25)
        self.click_element("paypal continue btn")
        self.wait_until_element_is_visible("place order", 80)
        self.mouse_over_element_in_viewport("place order")
        self.click_element("place order")
        self.wait_until_element_is_visible("xpath=(//h3[contains(text(), 'View my order')])")
        self.body_should_contain_text('Your order has been placed and a confirmation email has been sent - your order number is',
                                    "Expected order confirmation is not present")
        self.click_element("continue shopping")
        self.log_out()
        return self

    @robot_alias("Proceed_to_checkout_excluding_vat")
    def checkout_exluding_vat(self):
        self.choose_checkout_user("checkout guest")
        self.add_checkout_address(names=True, city='geneva')
        self.wait_until_element_is_visible("xpath=(//h2[contains(text(), 'Select your billing address')])")
        self.add_checkout_address(city='geneva')
        self.wait_until_element_is_visible("Livraison domicile (Suisse)")
        self.click_element("Livraison domicile (Suisse)")
        self.click_element("bank cheque")
        sleep(3)
        self.body_should_contain_text('YOUR ORDER IS EXEMPT FROM FRENCH VAT (VAT = 0%).', "Total price does not exclude VAT")
        self.find_element("xpath=(//div[@class='order_content'])")
        all_prices = self.get_webelements("xpath=(//p[@class='price_color change_curr'])")
        total_purchase = 0
        for item in all_prices:
            price = item.get_attribute('data-value')
            print price
            total_purchase += float(price)
            print total_purchase
        self.find_element("total product price excl vat")
        price_exl_vat = self.get_text("total product price excl vat")
        print price_exl_vat
        if len(price_exl_vat) >= 8 and price_exl_vat[-7] == ',':
            price_exl_vat = price_exl_vat.replace(',','')
        price_exl_vat = float(price_exl_vat[1:])
        print price_exl_vat
        asserts.assert_equal(round(total_purchase, 2), price_exl_vat, "Total price does not exclude VAT")
        self.find_element("total product price incl vat")
        price_inc_vat = self.get_text("total product price incl vat")
        if len(price_inc_vat) >= 8 and price_inc_vat[-7] == ',':
            price_inc_vat = price_inc_vat.replace(',','')
        price_inc_vat = float(price_inc_vat[1:])
        asserts.assert_not_equal(price_exl_vat, price_inc_vat, "Total price does not exclude VAT")
        self.mouse_over_element_in_viewport("place order")
        self.click_element("place order")
        self.wait_until_element_is_visible("continue shopping")
        self.click_element("continue shopping")
        return self

    def test_checkout_preview(self):
        preview_text = ['Shipping address', 'Billing address', 'Shipping method', 'Payment', 'Products']
        for item in preview_text:
            self.body_should_contain_text(item, '%s is not present in the preview of payment' % item)
        return self

    @robot_alias("Verify_unreferenced_product_label")
    def unreferenced_label(self):
        locator = ("xpath=(//div[@class='availability-label no_price'])")
        self.search_filter_labels("availability filter", 'unreferenced product', locator)
        return self

    @robot_alias("Verify_unreferenced_product_label_for_the_manufacture_of_medicated_feeds")
    def unreferenced_label_medicated_feeds(self):
        locator = ("xpath=(//div[@class='availability-label medicated_feeds'])")
        self.search_filter_labels("availability filter", 'unreferenced product (medicated feeds)', locator)
        return self

    @robot_alias("Verify_manufactoring_suspended_label")
    def manufacturing_suspended_label(self):
        locator = ("xpath=(//div[@class='availability-label manufactoring_suspended'])")
        self.search_filter_labels("availability filter", 'manufacturing suspended', locator)
        return self

    @robot_alias("Verify_manufactoring_stopped_label")
    def manufacturing_stopped_label(self):
        locator = ("xpath=(//div[@class='availability-label manufactoring_stopped'])")
        self.search_filter_labels("availability filter", 'manufacturing stopped', locator)
        return self

    @robot_alias("Verify_marketing_authorisation_suspended_label")
    def marketing_auth_suspended_label(self):
        locator = ("xpath=(//div[@class='availability-label marketing_auth_suspended'])")
        self.search_filter_labels("availability filter", 'marketing auth suspended', locator)
        return self

    @robot_alias("Verify_unavailable_out_of_stock_label")
    def unavailable_out_of_stock_label(self):
        locator = ("xpath=(//div[@class='availability-label unavailable_stock'])")
        self.search_filter_labels("availability filter", 'out of stock filter', locator)
        return self

    @robot_alias("Verify_prescription_required_label")
    def prescription_required_only_vets(self):
        locator = ("xpath=(//div[@class='availability-label prescription_only_vets'])")
        self.search_filter_labels("availability filter", 'prescription required', locator)
        return self

    @robot_alias("Verify_veterinary_drugs_label")
    def veterinary_drugs_label(self):
        locator = ("xpath=(//span[@class='is_drug availability-label'])")
        self.search_filter_labels("category filter", 'veterinary drugs', locator)
        return self

    @robot_alias("Verify_issuance_on_prescription_label")
    def issuance_on_prescription_label(self):
        locator = ("xpath=(//span[@class='sur-ordonnance availability-label'])")
        self.search_filter_labels("prescription filter", 'issuance on prescription', locator)
        return self

    @robot_alias("Verify_livestock_health_program_filter")
    def livestock_health_program_label(self):
        locator = ("xpath=(//span[@class='bilan-sanitaire LHP availability-label'])")
        self.search_filter_labels("livestock health program filter", 'LHP beef production', locator)
        return self

    def search_filter_labels(self, search_filter, subfilter_name, label_locator):
        self.click_element("all products")
        self.search_labels_in_pages(search_filter, subfilter_name, label_locator)
        if self._is_visible("xpath=(//li[@class='next'])") != None:
            second_page = self.find_elements("xpath=(//li[@class='next'])")
            self.search_labels_in_pages(search_filter, subfilter_name, label_locator, second_page[0])
        if self._is_visible("xpath=(//li[@class='new_page'])"):
            last_page = self.find_elements("xpath=(//li[@class='new_page'])")
            if len(last_page) == 2:
                self.search_labels_in_pages(search_filter, subfilter_name, label_locator, last_page[1])
        return self

    def search_labels_in_pages(self, search_filter, subfilter_name, label_locator, page=None):
        if page == None:
            self.wait_until_element_is_visible("search filters")
            self.click_element("search filters")
            self.click_element(search_filter)
            self.click_element(subfilter_name)
            sleep(1)
        else:
            self.click_element(page)
        search_results = self.find_elements("xpath=(//article[@class='product_pod'])")
        labels = self.find_elements(label_locator)
        asserts.assert_equal(len(labels), len(search_results), "Label %s is not found in some elements" % subfilter_name)
        return self

    def add_to_drug_request_unlogged(self, product):
        talk_to_pharmacist_btn = product.find_element_by_class_name('request_for_unlogged_users')
        self.mouse_over_element_in_viewport(talk_to_pharmacist_btn)
        self.click_element_at_coordinates(talk_to_pharmacist_btn, 0, 0)
        self.wait_until_element_is_visible("login for drug request")
        self.click_element("login for drug request")
        return self

    def add_to_drug_request_from_product_page(self):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('on prescription')
        self.select_with_LHP_filter()
        prod_name = self.product_preview_page()
        self.wait_until_element_is_visible("xpath=(//*[@id='add_to_drug_request_form_main']/button)")
        self.mouse_over_element_in_viewport("xpath=(//*[@id='add_to_drug_request_form_main']/button)")
        self.click_element("xpath=(//*[@id='add_to_drug_request_form_main']/button)")
        self.wait_until_element_is_visible("id=add-to-drug-reques-modal", 25)
        sleep(2)
        self.click_element("id=id_read_instructions")
        self.click_element("xpath=(//button[@value='Add to drug request'])")
        sleep(3)
        return prod_name

    def add_to_drug_request_from_listing(self):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('on prescription')
        product = self.select_product(True)
        pr_name = self.product_name(product)
        self.mouse_over_element_in_viewport(product)
        print pr_name
        drug_req = product.find_element_by_xpath(".//*[@id='add_to_basket_form_main']/button")
        self.mouse_over_element_in_viewport(drug_req)
        self.click_element_at_coordinates(drug_req, 0, 0)
        self.wait_until_element_is_visible("id=add-to-drug-reques-modal", 30)
        sleep(2)
        self.click_element("id=id_read_instructions")
        self.click_element("xpath=(//*[@id='add-to-drug-reques-modal']/div/div/div[3]/form/button)")
        sleep(3)
        self.body_should_contain_text(pr_name, 'Selected product was not added to wishlist')
        return pr_name

    def add_prescr_to_drug_request(self, prod_name):
        self.click_element("xpath=(//span[contains(text(),'Add prescription')])")
        self.focus("xpath=(//div[@class='modal-dialog'])")
        prescr_list = self.find_elements("xpath=(//div[@class='prescr_block border_block'])")
        for i in prescr_list:
            self.mouse_over_element_in_viewport(i)
            sleep(2)
            info = i.find_element_by_class_name('products')
            txt = self.get_text(info)
            if len(list(set(prod_name.lower()).symmetric_difference(set(txt.lower())))) == 0:
                checkbox = i.find_element_by_class_name('checkbox')
                sleep(1)
                self.click_element(checkbox)
                break
        sleep(3)
        self.mouse_over_element_in_viewport("OK btn for prescr in request")
        self.click_element_at_coordinates("OK btn for prescr in request", 0, 0)
        sleep(2)
        return self

    def drug_request_editing_page(self):
        self.mouse_over_element_in_viewport('user account')
        self.click_element_at_coordinates('user account', 0, 0)
        self.click_element('dashboard')
        self.click_element('dashboard health of animals')
        self.click_element('dashboard drug requests')
        sleep(1)
        self.click_element("edit drug request")
        return self

    def go_to_drug_requests_from_dashboard(self):
        self.back_to_website()
        self.click_element("my drug requests")
        sleep(1)
        self.click_element("list of drug requests")
        self.click_element("drug request link")
        sleep(2)
        return self

    def set_drug_request_status(self, status):
        self.mouse_over_element_in_viewport("id=select2-chosen-2")
        self.click_element_at_coordinates("id=select2-chosen-2", 0, 0)
        self.click_element(status)
        sleep(2)
        self.click_element("id=save-button")
        return self

    def edit_drug_request_product(self, comment):
        self.click_element("edit prod drug request")
        self.wait_until_element_is_visible('id=id_quantity')
        self.input_text('id=id_quantity', '25')
        sleep(2)
        self.input_text("id=id_pharmacist_comment", comment)
        sleep(1)
        self.click_element("id=create-button")
        return self

    def check_comments(self):
        self.click_element("drug request comments")
        all_comments = self.find_elements("xpath=(//div[@class='comment-text'])")
        self.mouse_over_element_in_viewport(all_comments[0])
        sleep(1)
        asserts.assert_equal(self.get_text(all_comments[0]).strip(), "Only two products can be bought",
            "The comment to drug request has been not added")
        asserts.assert_equal(self.get_text(all_comments[1]).strip(), "The drug request can be approved",
            "The comment to drug request product has been not added")
        return self

    @robot_alias("Add_drug_request_as_guest_user")
    def add_drug_request_with_one_product(self):
        self.click_element("all products")
        self.select_with_search_filters()
        self.select_with_prescription_filter('on prescription')
        product = self.select_product()
        pr_name = self.product_name(product)
        print pr_name
        self.add_to_drug_request_unlogged(product)
        self.successful_login()
        self.back_to_website()
        prod_name = self.add_to_drug_request_from_product_page()
        self.add_prescription(prod_name)
        self.wait_until_element_is_visible("my drug requests")
        self.click_element("my drug requests")
        sleep(1)
        self.body_should_contain_text(prod_name, "Product was not added to drug request")
        self.click_element("id=create-button")
        sleep(3)
        self.body_should_contain_text('You have chosen to use our website as means to provide a copy of your prescription. Please add this prescription.',
            "Drug request was created without prescription")
        self.add_prescr_to_drug_request(prod_name)
        self.input_text("xpath=(//input[@name='quantity'])", '2')
        sleep(2)
        self.mouse_over_element_in_viewport("id=create-button")
        self.click_element_at_coordinates("id=create-button", 0, 0)
        sleep(5)
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_false('Associated prescription does not contain selected product.' in body_txt,
            'The prescription does not include necessary products')
        sleep(2)
        return self

    @robot_alias("Add_comments_to_drug_request_and_check_rejected_status")
    def add_comments_and_reject(self):
        self.drug_request_editing_page()
        sleep(3)
        self.set_drug_request_status("reject drug request")
        self.go_to_drug_requests_from_dashboard()
        self.body_should_contain_text("Status: your drug request is rejected.",
            "Drug request status has been not changed to 'Rejected'")
        self.element_should_be_disabled("id=move-to-basket-button")
        self.drug_request_editing_page()
        self.edit_drug_request_product("Only two products can be bought")
        self.select_frame("id=id_pharmacist_comment_ifr")
        self.input_text("id=tinymce", "The drug request can be approved")
        self.unselect_frame()
        self.set_drug_request_status("approve drug request")
        new_status = self.find_element("xpath=(//tbody//tr[1]//td[3])")
        asserts.assert_equal(self.get_text(new_status), "Approved", "The drug request status has been not changed")
        return self

    @robot_alias("Write_comments_and_set_quantity_limitation")
    def write_comments_and_set_quantity(self):
        self.go_to_drug_requests_from_dashboard()
        self.body_should_contain_text("Status: your drug request is approved, you can move products to basket.",
            "The status has been not changed")
        sleep(1)
        self.check_comments()
        self.click_element("select all prods in drug request")
        sleep(1)
        self.click_element("id=move-to-basket-button")
        sleep(4)
        self.element_should_be_visible("my basket from request", "Product has been not added to basket")
        self.click_element("my basket from request")
        self.input_text("id=id_form-0-quantity", '50')
        self.click_element("update quantity in basket")
        sleep(2)
        self.element_should_be_visible("xpath=(//span[@class='error-block'])")
        sleep(2)
        self.input_text("id=id_form-0-quantity", '1')
        self.click_element("update quantity in basket")
        sleep(2)
        return self

    @robot_alias("Add_a_drug_request_as_logged_in_user")
    def add_drug_request_with_many_products(self):
        all_prods = []
        for i in range(2):
            prod_name = self.add_to_drug_request_from_listing()
            if len(all_prods) >= 2 and prod_name == all_prods[0]:
                new_name = self.add_to_drug_request_from_listing()
                print new_name
                all_prods.append(new_name)
            else:
                all_prods.append(prod_name)
            print all_prods
        self.add_prescription(all_prods)
        sleep(2)
        self.wait_until_element_is_visible("my drug requests")
        self.click_element("my drug requests")
        sleep(1)
        self.click_element("id=create-button")
        sleep(3)
        self.body_should_contain_text('You have chosen to use our website as means to provide a copy of your prescription. Please add this prescription.',
            "Drug request was created without prescription")
        list_pr = '\n'.join(all_prods)
        self.add_prescr_to_drug_request(list_pr)
        sleep(4)
        self.wait_until_element_is_visible("id=create-button")
        self.click_element("id=create-button")
        sleep(4)
        self.view_drug_request_from_website(list_pr)
        return all_prods


    @robot_alias("Edit_created_drug_request")
    def edit_drug_request(self, all_prods):
        self.click_element("edit drug request")
        sleep(3)
        el = self.find_elements("xpath=(//div[@class='drug-request-product'])")[0]
        removed_el_name = self.get_text(el.find_element_by_xpath(".//div[@class='name']//a")).lower()
        print removed_el_name
        remove = el.find_element_by_xpath(".//div[@class='remove-product']")
        self.click_element(remove)
        sleep(2)
        quantity = self.find_elements("xpath=(//input[@name='quantity'])")[0]
        self.input_text(quantity, '4')
        sleep(1)
        self.click_element("id=create-button")
        all_prods.remove(removed_el_name)
        print all_prods
        list_update = '\n'.join(all_prods)
        self.view_drug_request_from_website(list_update)
        edited_products = self.find_elements("xpath=(//div[@class='products'])")
        asserts.assert_false(removed_el_name in self.get_text(edited_products[1]),
            "The product %s was not deleted" % removed_el_name)
        quantity = self.find_elements("xpath=(//strong[@class='td_sales'])")
        asserts.assert_equal(self.get_text(quantity[0]), 'Quantity: 4', )
        self.body_should_contain_text("Status: your drug request is waiting for pharmacist's approval.",
            "Drug request status is not 'Wating for approval'")
        self.element_should_be_disabled("id=move-to-basket-button")
        return self

    @robot_alias("Set_'Approved'_drug_request_status")
    def set_drug_request_approved(self):
        self.drug_request_editing_page()
        sleep(3)
        self.set_drug_request_status("approve drug request")
        self.go_to_drug_requests_from_dashboard()
        self.body_should_contain_text("Status: your drug request is approved, you can move products to basket.",
            "The status has been not changed")
        self.click_element("select all prods in drug request")
        self.click_element("id=move-to-basket-button")
        sleep(4)
        self.element_should_be_visible("my basket from request", "Product has been not added to basket")
        self.click_element("my basket from request")
        return self

    @robot_alias("Delete_drug_request_at_dashboard")
    def delete_drug_request(self):
        self.click_element('dashboard health of animals')
        self.click_element('dashboard drug requests')
        sleep(2)
        self.click_element('delete drug request')
        sleep(3)
        delete_dr_request = self.find_elements('confirm delete drug request')
        self.click_element(delete_dr_request[0])
        sleep(2)
        return self

    @robot_alias("Proceed_to_checkout_with_shipping_method_limitation")
    def checkout_pickup_at_pharmacy_only(self):
        self.click_element("proceed to checkout button")
        self.mouse_over_element_in_viewport("proceed in checkout")
        self.click_element_at_coordinates("proceed in checkout", 0, 0)
        self.click_element("checkout company Quinta")
        self.click_element("proceed company checkout")
        self.choose_existing_address(".//button[contains(concat(' ', normalize-space(@class), ' '), ' ship-to-this-address-tbutton')]")
        self.choose_existing_address(".//button[contains(concat(' ', normalize-space(@class), ' '), ' select-billing-address-tbutton')]")
        asserts.assert_equal(len(self.find_elements("xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' select-method-tbutton')])")), 1,
            "More than one shipping methods are available")
        self.click_element("xpath=(//button[contains(concat(' ', normalize-space(@class), ' '), ' select-method-tbutton')])")
        self.click_element("during pickup payment")
        self.test_checkout_preview()
        self.mouse_over_element_in_viewport("place order")
        self.click_element("place order")
        sleep(2)
        self.click_element("continue shopping")
        sleep(3)
        self.delete_prescription()
        return self

    def choose_existing_address(self, select_address_btn):
        addresses = self.find_elements("xpath=(//dd[@class='well'])")
        for i in addresses:
            if len(i.find_elements_by_xpath(".//span[contains(text(), 'Lyon')]")) != 0:
                add_address = i.find_element_by_xpath(select_address_btn)
                self.mouse_over_element_in_viewport(add_address)
                self.click_element_at_coordinates(add_address, 0, 0)
                sleep(3)
                break
        return self

    def view_drug_request_from_website(self, list_pr):
        prescr = self.find_elements("xpath=(//div[@class='drug_request_list']//tbody//tr)")
        for i in prescr:
            info = i.find_element_by_class_name("product_name")
            if len(list(set(list_pr.lower()).symmetric_difference(set(self.get_text(info).lower())))) == 0:
                view = i.find_element_by_class_name('drug_request_link')
                self.click_element(view)
                sleep(4)
                break
        return self

    @robot_alias("Proceed_to_checkout_with_paybox_payment")
    def checkout_with_paybox_payment(self):
        self.click_element("proceed to checkout button")
        self.element_should_be_visible("xpath=(//div[@class='alert alert-warning text-center'])",
            "Prescription should be required")
        self.mouse_over_element_in_viewport("proceed in checkout")
        self.click_element("proceed in checkout")
        self.wait_until_element_is_visible("checkout company Quinta")
        self.click_element("checkout company Quinta")
        self.click_element("proceed company checkout")
        self.add_checkout_address(city='berlin')
        self.wait_until_element_is_visible("xpath=(//h2[contains(text(), 'Select your billing address')])")
        self.add_checkout_address(city='berlin')
        self.wait_until_element_is_visible("home delivery items")
        self.click_element("home delivery items")
        self.click_element("home delivery(Ger, Bel, Lux)")
        self.wait_until_element_is_visible("select paybox")
        self.click_element("select paybox")
        self.wait_until_element_is_visible("paybox cardnumber")
        self.type_in_box('1111222233334444', "paybox cardnumber")
        self.type_in_box('123', "paybox ccv number")
        self.click_element("continue paybox payment")
        self.test_checkout_preview()
        self.mouse_over_element_in_viewport("place order")
        self.click_element("place order")
        self.wait_until_element_is_visible("continue shopping")
        self.click_element("continue shopping")
        sleep(2)
        self.delete_prescription()
        return self

    def delete_prescription(self):
        self.click_element('user account')
        self.click_element('dashboard')
        self.click_element('dashboard health of animals')
        self.click_element("dashboard prescriptions")
        self.click_element("delete prescription at dashboard")
        sleep(2)
        self.click_element("delete prescription")
        sleep(2)
        return self

    @robot_alias("Scroll_to_element")
    def mouse_over_element_in_viewport(self, locator):
        if isinstance(locator, str):
            element = self.find_element(locator)
        else:
            element = locator
        self.driver.execute_script('return arguments[0].scrollIntoView();', element)
        self.driver.execute_script("window.scrollBy(0, -150);")
        self.wait_until_element_is_visible(element)
        self.mouse_over(element)
        return self

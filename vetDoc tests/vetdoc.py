# -*- coding: utf-8 -
from robotpageobjects import Page, robot_alias
from robot.utils import asserts
from time import sleep
import random

class VetDocHomePage(Page):
    """ Models the VetDoc home page at:
        HOST://vet-directory.devel.vetopharm.quintagroup.com"""


    # Allows us to call this page
    # something other than the default "VetDoc Home Page"
    # at the end of keywords.
    name = "VetDoc"

    result_msg = 'no results matching your query'

    # inheritable dictionary mapping human-readable names
    # to Selenium2Library locators. You can then pass in the
    # keys to Selenium2Library actions instead of the locator
    # strings.
    selectors = {
        "address input box": "id=id_all",
        "name input box": "id=id_name",
        "language menu": "xpath=(//span[@class='navbar-toggler-icon'])",
        "fr button": "id=fr-lang-button",
        "en button": "id=en-lang-button",
        "remove location": "xpath=(//div[@class='remove-loc']/i[@class='fa fa-times'])",
        "remove name": "xpath=(//div[@class='remove-name']/i[@class='fa fa-times'])",
        "dropdown": "xpath=(.//*[@id='react-select-2--value-item'])",
        "select clinic": "xpath=(.//*[@id='react-select-2--option-1'])",
        "location map": "xpath=(//div[@class='GMap'])",
        "search results": "xpath=(//div[@class='row']/ul/li)",
        "species option": "xpath=(//div[@class='Select-placeholder'][contains(text(),'Species')])",
        "specialty option": "xpath=(//div[@class='Select-placeholder'][contains(text(),'Specialty')])",
        "list of species": "id=react-select-3--list",
        "list of specialties": "id=react-select-4--list",
        "species": "xpath=(//div[@class='specie-checked']//i[@class='fa fa-times'])",
        "specialty": "xpath=(//div[@class='spec-checked']//i[@class='fa fa-times'])",
        "clear all btn": "xpath=(//button[@class='btn-clear-all'])",
        "dropdown arrow": "xpath=(.//*[@id='react-select-5--value-item'])",
        "switch to clinic": "xpath=(.//*[@id='react-select-5--option-1'])",
        "search results count": "xpath=(//div[@class='result-count text-center'])",
        "address map": "id=map",
        "filter tags": "xpath=(//ul[@class='specialities']/a)",
        "list of clinics": "xpath=(//ul[@class='clinics']/li)",
        "list of veterinarians": "xpath=(//ul[@class='veterinarians']/li)",
        "phone": "xpath=//div[@class='clinic_tel']/a",
        "distance filter": "xpath=//div[@class='block-within']//div[@class='Select-control']//span[@class='Select-arrow-zone']",
        "search radius": "id=react-select-8--list",
        "last page": "xpath=//div/div[4]/div[3]/nav/ul/li[10]"
    }
    

    def type_in_search_box(self, txt, search_box):
        for i in range(len(txt)):
            self.input_text(search_box, txt[0:i+1])
            sleep(1)

        # We always return something from a page object, 
        # even if it's the same page object instance we are
        # currently on.
        return self

    def address_value(self):
        return random.choice(["Par", "Lon", "Tem", "Pen", "Del", "Har", "Rec", "Cap", "For"])

    def clinic_value(self):
        return random.choice(["clinique", "societe", "selarl", "cabinet", "termes", "civile"])

    def veterinarian_value(self):
        return random.choice(["Pauline", "Stephan", "Enri", "Vincent", "Adeline", "Igor", "Nicolas", "Dominique"])

    @robot_alias("maximize__window")
    def maximize_browser_window(self):
        self._current_browser().maximize_window()
        return self
    
    @robot_alias("back__to__previous__page")
    def navigate_back(self):
        self._current_browser().back()
        return self

    @robot_alias("switch__between__languages")
    def change_language(self):
        self.select_french()
        self.click_element("language menu")
        self.select_english()
        return self

    @robot_alias("select__french__language")
    def select_french(self):
        self.click_element("language menu")
        self.click_button("fr button")
        body_txt= self.get_text("css=body").encode("utf-8")
        asserts.assert_true("Espèce" in body_txt, "French was not selected")
        return self

    def select_english(self):
        self.click_button("en button")
        self.body_should_contain_text("Species", "English was not selected")
        return self

    @robot_alias("clear__address__field")
    def clear_location_field(self):
            self.clear_field("remove location","address input box")
            return self

    @robot_alias("clear__name__field")
    def clear_name_field(self):
            self.clear_field("remove name","name input box")
            return self

    def clear_field(self, field_locator, box_locator):
        self.click_element(field_locator)
        box_value= self.find_element(box_locator).get_attribute('value')
        asserts.assert_true(box_value =="", 
            "The delete button did not empty the search field")
        return self

    @robot_alias("search__by__address")
    def search__by__address(self):
        address= self.address_value()
        self.type_in_search_box(address,"address input box")
        index= self.test_autocomplete("xpath=(//div[@class='pac-container pac-logo'])", address)
        city_name= self.get_text("xpath=/html/body/div[2]/div["+str (index)+"]/span[2]")
        self.click_element("xpath=/html/body/div[2]/div["+str (index)+"]")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        if self.result_msg in body_txt: self.search__by__address()
        else: self.body_should_contain_text (city_name, 
            "The search results do not include the inquired city name")
        return self

    @robot_alias("search__by__name")
    def search__by__name(self, term):
        self.type_in_search_box(term, "name input box")
        index= self.test_autocomplete("xpath=//*[@id='id_list_name']", term[:4])
        name= self.get_text("xpath=//*[@id='id_list_name']/li["+str (index)+"]/a/span")
        self.click_element("xpath=//*[@id='id_list_name']/li["+str (index)+"]")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        if self.result_msg in body_txt: self.search__by__name(term)
        else: self.body_should_contain_text(name, 
            "Page was not redirected to the corresponding profile")
        return self

    def test_autocomplete(self, autocomplete, txt):
        autocomplete_text= self.get_text(autocomplete).lower().splitlines()
        sleep(2)
        for element in autocomplete_text:
            asserts.assert_true(txt.lower() in element, 
                "Autocomplete list contains suggestions other than %s" %txt)
        index= random.randint(1,len(autocomplete_text))
        return index

    @robot_alias("switch__between__clinics__and__veterinarians")
    def select_category(self):
        self.click_element("dropdown")
        self.click_element("select clinic")
        asserts.assert_true("Clinic" in self.get_text("dropdown"), 
            "Clinic option was not selected from the dropdown menu")
        return self

    @robot_alias("Show__map")
    def show_location_map(self, map_selector):
        asserts.assert_true(self.is_visible(map_selector), 
            "Map is not displayed")
        return self

    @robot_alias("show__distance__from__location")
    def distance_from_location(self):
        for address in self.find_elements("search results"):
            asserts.assert_true("km from" in self.get_text(address), 
                "The address does not include distance from the search location")
        return self

    @robot_alias("search__by__species")    
    def species_search(self):
        self.click_element("species option")
        index= random.randrange(0, len(self.get_text("list of species").splitlines()))
        selected_species= self.get_text("id=react-select-3--option-"+str (index)+"")
        self.click_element("id=react-select-3--option-"+str (index)+"")
        self.check_search_result(selected_species)
        return self

    @robot_alias("search__by__specialty")
    def specialty_search(self):
        self.click_element("specialty option")
        index= random.randrange(0, len(self.get_text("list of specialties").splitlines()))
        selected_specialty= self.get_text("id=react-select-4--option-"+str (index)+"")
        self.click_element("id=react-select-4--option-"+str (index)+"")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        if self.result_msg in body_txt: 
            self.delete_filters("specialty") 
            self.specialty_search()
        else: 
            self.check_search_result(selected_specialty)
        return self

    def check_search_result(self, filter_tag):
        for info_block in self.find_elements("search results"):
            asserts.assert_true(filter_tag in self.get_text(info_block), 
                "Search results do not include %s information" %filter_tag)
        return self

    @robot_alias("clear__all__search__filters")
    def clear_all(self):
        self.delete_filters("clear all btn")
        return self

    @robot_alias("clear__search__filter") 
    def delete_filters(self, filter_tag):
        previous_quantity= len(self.get_text("search results count"))
        self.click_element(filter_tag)
        current_quantity= len(self.get_text("search results count"))
        asserts.assert_false(previous_quantity==current_quantity or self.is_visible(filter_tag), 
            "Search filter was not cleared")
        return self

    @robot_alias("switch__to__clinic__search")
    def choose_from_dropdown(self):
        self.click_element("dropdown arrow")
        self.click_element("switch to clinic")
        search_results= self.get_text("search results count")
        asserts.assert_true("clinics" in search_results, 
            "Veterinarian/Clinic drop-down did not change results display")
        return self

    @robot_alias("check__if__search__filters__are__cleared")
    def check_search_filters(self):
        asserts.assert_false(self.is_visible("species"), 
            "Search filter was not cleared")
        return self

    @robot_alias("go__to__selected__profile")
    def go_to_profile(self):
        index= random.randrange(0, len(self.find_elements("search results")))
        selected_item= self.get_text("xpath=(//*[@id='el-"+str (index)+"']//div[@class='vet_info']/a)").lower()
        self.click_element("xpath=(//*[@id='el-"+str (index)+"']//div[@class='vet_info']/a)")
        self.body_should_contain_text(selected_item, 
            "Page was not redirected to the corresponding profile")
        return self

    @robot_alias("check__species__option")
    def check_search_option(self):
        option= random.choice(self.find_elements("filter tags"))
        tag= self.get_text(option)
        self.click_element(option)
        self.check_search_result(tag)
        return self

    @robot_alias("open__clinic__profile")
    def lead_to_clinic_profile(self):
        if len(self.find_elements("list of clinics")) > 1:
            index= random.randint(1, len(self.find_elements("xpath=(//ul[@class='clinics']/li)")))
            selected_clinic= self.get_text("xpath=(//ul[@class='clinics']/li["+ str(index) +"]//a)")
            self.click_element("xpath=(//ul[@class='clinics']/li["+ str(index) +"]//a)")
        else:           
            selected_clinic= self.get_text("xpath=(//ul[@class='clinics']/li//a)")
            self.click_element("xpath=(//ul[@class='clinics']/li//a)")
        self.body_should_contain_text(selected_clinic, 
            "Page was not redirected to the corresponding profile")
        return self

    @robot_alias("open__veterinarian__profile")
    def lead_to_veterinarian_profile(self):
        index= random.randint(1, len(self.find_elements("list of veterinarians")))
        selected_vet= self.get_text("xpath=(//ul[@class='veterinarians']/li["+ str(index) +"]//a)")
        self.click_element("xpath=(//ul[@class='veterinarians']/li["+ str(index) +"]//a)")
        self.body_should_contain_text(selected_vet, 
            "Page was not redirected to the corresponding profile")
        return self

    @robot_alias("check__contact__number")
    def check_phone_number(self):
        self.wait_until_page_contains_element("phone")
        phone_number= (self.get_text("phone"))[1:]
        app_link= self.find_element("xpath=//div[@class='clinic_tel']/a[@href='tel:+33 (0)"+ str(phone_number) +"']")
        self.click_element(app_link)
        return self

    @robot_alias("check__distance__filter")
    def change_search_radius(self):
        self.type_in_search_box('Lyon',"address input box")
        self.click_element("xpath=/html/body/div[2]/div[1]")
        self.click_element("distance filter")
        self.select_radius()
        return self

    def select_radius(self):
        index=0
        for i in range(0, len(self.get_text("search radius").splitlines())):
            search_radius= int(self.get_text("id=react-select-8--option-"+str (index)+"")[:-2])
            self.click_element("id=react-select-8--option-"+str (index)+"")
            self.check_distance(search_radius)
            self.click_element("distance filter")
            index += 1
        return search_radius

    def check_distance(self, search_radius):
        self.click_element("last page")
        html_list = self.find_element("xpath=(//div[@class='row']/ul)")
        items = html_list.find_elements_by_tag_name("li")
        for vet_info in items:
            location= self.get_text(vet_info).splitlines()[-1]
            if 'km' in location:
                radius= location[:-21]
                asserts.assert_true(float(radius) < search_radius,
                    "The address does not include distance from the search location")
        return self


    @robot_alias("body_should_contain")
    def body_should_contain_text(self, str, error_message, ignore_case=True):
        result_msg = str.lower() if ignore_case else str
        result_msg = result_msg.encode("utf-8")
        body_txt = self.get_text("css=body").encode("utf-8").lower()
        asserts.assert_true(result_msg in body_txt, error_message)
        return self

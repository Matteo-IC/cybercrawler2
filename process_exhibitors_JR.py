import dataclasses

import pydantic_core
from pydantic.dataclasses import dataclass
import json
import requests
from bs4 import BeautifulSoup

base = "https://jaarbeurszakelijk.app.swapcard.com"

class_company_name = "dbnofQ"
class_company_info = "gbyhbR"
class_segment = "gShnkr"
class_contact = "btWXRc"
class_social_media = "kzrhIj"


@dataclass
class Company():
    name: str = ''
    address: str = ''
    country: str = ''
    segments: set[str] = dataclasses.field(default_factory=set)
    social_media: list[str] = dataclasses.field(default_factory=list)
    websites: list[str] = dataclasses.field(default_factory=list)
    emails: list[str] = dataclasses.field(default_factory=list)
    telephones: list[str] = dataclasses.field(default_factory=list)
    information: list[str] = dataclasses.field(default_factory=list)

    def init_from_soup(self, soup: BeautifulSoup):
        self.find_info(soup)
        self.find_contact_details(soup)

    def find_info(self, soup):
        name_element = soup.find(class_=class_company_name)
        if name_element:
            self.name = name_element.text

        info_element = soup.find(class_=class_company_info)
        if info_element:
            paragraphs = info_element.find_all('p')
            for p in paragraphs:
                self.information.append(p.text)

    def find_contact_details(self, soup: BeautifulSoup):
        contact_elements = soup.findAll(class_=class_contact)
        if contact_elements:
            for contact_element in contact_elements:
                contact_element_text = contact_element.text
                if '@' in contact_element_text:
                    self.emails.append(contact_element_text)
                elif 'https' in contact_element_text:
                    self.websites.append(contact_element_text)
                elif '+' in contact_element_text:
                    self.telephones.append(contact_element_text)
                elif ',' in contact_element_text:
                    self.country = contact_element_text.split(',')[-1]
                    self.address = contact_element_text
                else:
                    pass



companies = []

with open("exhibitor_urls.txt") as f:
    for widget in f.readlines():
        url = base + widget.strip()
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            contents = response.text
            soup = BeautifulSoup(contents, "html.parser")
            company = Company()
            company.find_info(soup)
            company.find_contact_details(soup)
            companies.append(company)
        if len(companies) > 5:
            break

out = json.dumps(companies, default=pydantic_core.to_jsonable_python)
print(out)
            
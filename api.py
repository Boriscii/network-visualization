import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import json
# import config

API_TOKEN = 'YOUR_KEY_HERE'
FIND_ID_URL = 'https://api.companieshouse.gov.uk/search/companies?q={}'
FIND_OFFICERS_URL = 'https://api.companieshouse.gov.uk/company/{}/officers'
SIGN_CONTR_URL = 'https://api.companieshouse.gov.uk/company/{}/persons-with-significant-control'

headers = {'Authorization': API_TOKEN}


def get_company_number(company_name):
    '''FIND COMPANY_ID FROM QUERY_STRING'''
    find_id = requests.get(FIND_ID_URL.format(company_name), headers=headers)

    list_of_company_names = []
    for i in range(len(find_id.json()['items'])):
        list_of_company_names.append(find_id.json()['items'][i]['title'])

    print(list_of_company_names[:5])
    company_index = input("Enter the index of the company you want in the list: ")

    company_number = find_id.json()['items'][int(company_index)]['company_number']
    title = find_id.json()['items'][int(company_index)]['title']

    return company_number, title


def significant_control(company_number):
    '''FIND PERSONS WITH SIGNIFICANT CONTROL FOR A GIVEN COMPANY'''
    sign_contr = requests.get(SIGN_CONTR_URL.format(company_number), headers=headers)
    
    try:
        address_fields = ['premises', 'address_line_1', 'address_line_2', 'postal_code', 'locality', 'region', 'country']
        address_dict = sign_contr.json()['items'][0]['address'] # Access the address dict of JSON object
        address_str = ''

        # Remove non-existent address fields from the list
        for i in address_fields:
            if not i in address_dict:
                address_fields.remove(i)
                continue

            # Add address fields to the address string
            address_str += i + ': ' + address_dict[i] + ', '
        address_str = address_str.strip(' ,')

    except:
        address_str = 'Unknown address'

    # try:
    #     names = []

    #     for i in range(len(sign_contr.json()['items'])):
    #         name_dict = sign_contr.json()['items'][i]['name_elements']
    #         # print(i, name_dict)
    #         if 'title' not in name_dict:
    #             name_str = name_dict['forename'] + ' ' + name_dict['surname']
    #         else:
    #             name_str = name_dict['title'] + ' ' + name_dict['forename'] + ' ' + name_dict['surname']
    #         names.append(name_str)
    # except KeyError:
    #     names = 'No persons with significant control found'

    return address_str


def find_officers(company_number):
    '''FIND OFFICER'S COMPANIES FROM THEIR NAME'''
    req = urllib.request.Request(FIND_OFFICERS_URL.format(company_number), headers=headers)
    response = urllib.request.urlopen(req)

    webContent = response.read()
    director_info = json.loads(webContent)['items']

    # Obtain the link to director profile and append to list
    director_links = []
    director_names = []
    for i in range(len(director_info)):
        link = director_info[i]['links']['officer']['appointments']
        name = director_info[i]['name']
        director_links.append(link)
        director_names.append(name)

    # For each director's link get a list of their companies
    all_appointments = {}
    for name, link in zip(director_names, director_links):
        director_url = 'https://beta.companieshouse.gov.uk' + link
        dir_req = urllib.request.Request(director_url, headers=headers)
        dir_response = urllib.request.urlopen(dir_req)
        html = dir_response.read()
        soup = BeautifulSoup(html, 'html.parser')

        appointments = []
        for entry in soup.find(class_="appointments-list").descendants:
            if(entry.name == 'a'):

                # Only keep the "a" tags with company numbers, discard all others
                num_in_tag = any(digit.isdigit() for digit in entry.string)

                if num_in_tag:
                    companyNumber = re.findall(r'\d+', entry.string)[0]
                    companyName = ' '.join(re.findall('[a-zA-Z]+', entry.string))
                    appointment_dict = {companyNumber: companyName}
                    appointments.append(appointment_dict)

        all_appointments[name] = appointments
    
    names = all_appointments.keys()
    companies = all_appointments.values()
    return names, companies
    # return all_appointments

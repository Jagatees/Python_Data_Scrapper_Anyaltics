import time
from bs4 import BeautifulSoup
import json
import math
import requests
import asyncio
from requests_html import AsyncHTMLSession
from multiprocessing import cpu_count, Pool, freeze_support, Lock

type_room = []
title_room = []
links_room = []
sub_heading_room = []
description_room = []
price_list_room = []
day = []
month = []
year = []

FIRST_PAGE_NUMBER = 1

def get_request_home_page_website(website):
    return requests.get(website)

def get_content_website(soup, element, _class):
    return soup.find(element, class_=_class)

def count_max_page(page_count):
    return math.ceil(int(page_count.get_text()) / 10)

def get_request_page_range(int):
    urls_x = []
    for index in range(1, int):
        urls_x.append(f'https://rentinsingapore.com.sg/rooms-for-rent/page-{index}')
    return urls_x

def element_scrapping(index):
    page = requests.get(index)
    soup = BeautifulSoup(page.text, "html.parser")

    if page.status_code == 200:
        room_wide_listing_container = soup.find_all('div', class_='room__wide listing-container')
        room_sub_location = soup.find_all('h3', class_='room-sublocation mobile-room-sublocation')
        price = soup.find_all('div', class_='room-price')
        for div in room_sub_location:
            remove_text = div.get_text()
            remove_text = remove_text.strip().split('-')
            type_room.append(remove_text[0])
            title_room.append(remove_text[1])
        for div in room_wide_listing_container:
            a_tags_link = div.find_all('a')
            for a_tag in a_tags_link:
                link = 'https://rentinsingapore.com.sg/rooms-for-rent' + a_tag['href']
                links_room.append(link)
                a_tags_title = a_tag['title']
                sub_heading_room.append(a_tags_title)
        for div in price:
            price_text = div.get_text().strip()
            price_list_room.append(price_text)
    else:
        None

    data = [
        {
            'UID': i,
            'Price': price_list_room[i],
            'Type': type_room[i],
            'Title': title_room[i],
            'Links': links_room[i],
            'Sub Heading': sub_heading_room[i],
        }
        for i in range(len(title_room))
    ]

    with open("scrap.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

# Deep Crawling
dc_title = []
dc_description = []
dc_location = []
dc_details = []
links_testing = []
day = []
month = []
year = []

# Create a lock to synchronize file writes
file_lock = Lock()

def store_url():
    with open('scrap.json', 'r') as json_file:
        file_data = json.load(json_file)

        urls_y = []
        for index in file_data:
            urls_y.append(index['Links'])
        return urls_y

def content_html(url):
    try:
        page = requests.get(url)
        links_testing.append(str(url))
        soup = BeautifulSoup(page.text, "html.parser")
        response = requests.get(url)

        if response.status_code == 200:
            title_fp = soup.find('h1')
            dc_title.append(title_fp.get_text() if title_fp else "")

            room_details_div = soup.find('div', class_='room-details')
            li_elements = room_details_div.find_all('li')
            li_text_list = [li.get_text() for li in li_elements]
            dc_details.append(li_text_list)
            time = dc_details[0][0].split('on ', 1)[1].split('.')
            day.append(time[0])
            month.append(time[1])
            year.append(time[2])

            location_fp = soup.find(class_='room-street')
            dc_location.append(location_fp.get_text() if location_fp else "")

            description_elements = soup.find(class_='room-description')
            description_text = description_elements.get('description-text')
            dc_description.append(description_text)

        deep_crawling_data = [
            {
                'UID': str(i),
                'Title': dc_title[i],
                'Location': dc_location[i],
                'Tags': dc_details[i],
                'Links': links_testing[i],
                'Description': dc_description[i],
                'Day': day[i],
                'Month': month[i],
                'Year': year[i]
            }
            for i in range(len(dc_title))
        ]

        # Use the lock to ensure only one process writes to the file at a time
        with file_lock:
            with open("deep_crawl.json", "w") as json_file:
                json.dump(deep_crawling_data, json_file, indent=4)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main_scrawling_hopeing():
    urls = store_url()

    for index in urls:
        content_html(index)

if __name__ == '__main__':
    freeze_support()
    
    print('starting')
    start = time.perf_counter()
    
    request_web = get_request_home_page_website('https://rentinsingapore.com.sg/rooms-for-rent')
    soup = BeautifulSoup(request_web.text, "html.parser")

    total_count = get_content_website(soup, 'span', 'total-count')
    max_number_page = count_max_page(total_count)

    x = get_request_page_range(max_number_page)
    
    with Pool(cpu_count()) as p:
        p.map(element_scrapping, x)
    
    fin = time.perf_counter() - start
    print('Time Taken for Scraping: ' + str(fin))
    
    start = time.perf_counter()
    main_scrawling_hopeing()
    fin = time.perf_counter() - start
    print('Time Taken for Deep Crawling: ' + str(fin))

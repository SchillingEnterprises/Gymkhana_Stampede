# Created by: Gavin Schilling
# Purpose: Webscrape Gallopalooza horse images

from random import randint
from time import sleep, time
from warnings import warn

from IPython.core.display import clear_output
from bs4 import BeautifulSoup
from requests import get

# Preparing the monitoring of the loop
start_time = time()
horse_image_number = 0
requests = 0

# Make a get request
url = 'http://gallopalooza.com/showcase/statue/?id=132'
response = get(url)
data = response.text
# print(data)

html_soup = BeautifulSoup(response.text, 'html.parser')
# type(html_soup)

horse_images = html_soup.find_all('img', class_='horse-detail')
# print(type(horse_images))
# print(len(horse_images))

for number_of_horse_images in horse_images:
    horse_image_link = horse_images[horse_image_number]
    print(horse_image_link)
    horse_image_number += 1

    # Pause the loop
    sleep(randint(8, 15))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Break the loop if the number of requests is greater than expected
    if requests > len(number_of_horse_images) + 1:
        warn('Number of requests was greater than expected.')
        break

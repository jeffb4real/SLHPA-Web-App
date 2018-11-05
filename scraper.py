import csv
from selenium import webdriver

# Crawling Pages with Selenium (Part 1/2)
# https://www.youtube.com/watch?v=zjo9yFHoUl8


# Instantiate Chrome Browser and open URL
driver = webdriver.Chrome()
baseURL = "https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true"
driver.get(baseURL)

# Scrape all URLS on this page
links = driver.find_elements_by_partial_link_text('sanle')

# Print out all the scraped links
for i in range(len(links)):
    print (links[i].text)

driver.close()

# How to navigate through all photo archive pages:
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?      te=ASSET&isd=true
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=12&te=ASSET&isd=true
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=24&te=ASSET&isd=true
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=36&te=ASSET&isd=true
# ...
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=2520&te=ASSET&isd=true


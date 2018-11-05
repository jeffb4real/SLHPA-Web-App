import csv
from selenium import webdriver

# Crawling Pages with Selenium (Part 1/2)
# https://www.youtube.com/watch?v=zjo9yFHoUl8

# We will augment this URL to navigate to successive pages
baseURL = "https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true"

driver = webdriver.Chrome()
#for page in range (0, 2521, 12):
for page in range (0, 25, 12):
    # Instantiate Chrome Browser and open URL
    driver.get(baseURL + '&rw=' + str(page))

    # Scrape all URLS on this page and all successive pages
    links = driver.find_elements_by_partial_link_text('sanle')

    # Save the scraped links in a file
    with open('links.csv', 'a') as f:
        for i in range(len(links)):
            print (links[i].text)
            f.write ((links[i].text) + "\n")

driver.close()


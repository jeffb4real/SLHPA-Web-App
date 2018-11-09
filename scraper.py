import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Crawling Pages with Selenium (Part 1/2)
# https://www.youtube.com/watch?v=zjo9yFHoUl8

# We will augment this URL to navigate to successive pages
baseURL = "https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true"

driver = webdriver.Chrome()

#for page in range (0, 2521, 12):
#for page in range (0, 25, 12):
for page in range (0, 12, 12):
    # Instantiate Chrome Browser and open URL for this page
    driver.get(baseURL + '&rw=' + str(page))

    # Scrape all URLS on this page and all successive pages
    list_of_records = driver.find_elements(By.XPATH, "//img[contains(@id,'syndetics')]")

for record_index in range(0, len(list_of_records), 1):
    # Open the white sub-page for this record
    print ("record_index: " + str(record_index))
    record = list_of_records[record_index]
    record.click()
    time.sleep(1)

    # Scrape resource name and print it
    # .find_elementS PLURAL!!!
    resource_name = record.find_elements(By.XPATH,
    #    "//div[@class='displayElementText RESOURCE_NAME'][contains(text(),'pdf')]")
        "//div[@class='displayElementText RESOURCE_NAME']")
    print ('array size: ' + str(len(resource_name)))
    print (resource_name[record_index].text)

    # Save the scraped info to a file
    # with open('records.csv', 'a') as f:
    #     for i in range(len(links)):
    #         print (links[i].text)
    #         f.write ((links[i].text) + "\n")

    # Locate the white sub-page close button and click it.
    # Notice str(record_index), because each sub-page close button is unique!
    close_button = record.find_element(By.XPATH, "//div[@class='ui-dialog ui-widget ui-widget-content ui-corner-all detailModalDialog detailDialog" + str(record_index) + "']//span[@class='ui-icon ui-icon-closethick'][contains(text(),'close')]")
    close_button.click()
    time.sleep(3)

driver.close()

# >>> dir(links[0])
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
# '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__redu
# ce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_exec
# ute', '_id', '_parent', '_upload', '_w3c', 'clear', 'click', 'find_element', 'find_element_by_class_name', 'find_elem
# ent_by_css_selector', 'find_element_by_id', 'find_element_by_link_text', 'find_element_by_name', 'find_element_by_par
# tial_link_text', 'find_element_by_tag_name', 'find_element_by_xpath', 'find_elements', 'find_elements_by_class_name',
#  'find_elements_by_css_selector', 'find_elements_by_id', 'find_elements_by_link_text', 'find_elements_by_name', 'find
# _elements_by_partial_link_text', 'find_elements_by_tag_name', 'find_elements_by_xpath', 'get_attribute', 'get_propert
# y', 'id', 'is_displayed', 'is_enabled', 'is_selected', 'location', 'location_once_scrolled_into_view', 'parent', 'rec
# t', 'screenshot', 'screenshot_as_base64', 'screenshot_as_png', 'send_keys', 'size', 'submit', 'tag_name', 'text', 'va
# lue_of_css_property']

# 1.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true#

# 2.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f7395/1/1/0?te=ASSET&isd=true

# 3.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f7396/2/2/0?te=ASSET&isd=true

# 4.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f7397/3/3/0?te=ASSET&isd=true

# 13.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=12&te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f7406/0/0/1?rw=12&te=ASSET&isd=true

# 14.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=12&te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f7407/1/1/1?rw=12&te=ASSET&isd=true

# 2526.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=2520&te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f6409/5/5/210?rw=2520&te=ASSET&isd=true


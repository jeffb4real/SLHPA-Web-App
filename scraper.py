import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# We will augment this URL to navigate to successive search pages
baseURL = "https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true"

driver = webdriver.Chrome()

# Used to identify close button on sub-pages
# 2526 records total, numbered 0 through 2525.
count = 2520    # last page
count = 2508    # 2nd to last page
count = 0       # begin at beginning
count = 108     # problematic record 110.
count = 2496    # 3rd to last page

# Iterate over all search pages
#for page in range (count, 2521, 12):       # all pages
#for page in range (count, 12, 12):         # first page only
#for page in range (count, 2521, 12):       # last page only
#for page in range (count, 2521, 12):       # last two pages only
#for page in range (count, 25, 12):         # first three pages
#for page in range (count, 2521, 12):       # all pages
#for page in range (count, 108+12, 12):       # begin page ten, record 109. **THE BUG IS RECORD 110.**
for page in range (count, 2521, 12):       # last three pages only; first record here showed BUG

    # Open URL for this search page
    driver.get(baseURL + '&rw=' + str(page))

    # This XPath returns an iterable list of records found on this search page
    list_of_records = driver.find_elements(By.XPATH, "//div[contains(@id,'syndeticsImg')]")


    # All search pages return 12 records; except the last page, which has only 6 records
    #for record_index in range(0, 2, 1):    # only look at first few records
    for record_index in range(0, len(list_of_records), 1):

        # Open the white sub-page for this record
        print ("record_index: " + str(record_index))
        record = list_of_records[record_index]
        record.click()
        time.sleep(1)

        ###########################
        # DETAILS
        ###########################

        # .find_elementS PLURAL!!!

        # Resource Name
        #//div[@class='displayElementText RESOURCE_NAME']
        resource_name = record.find_elements(By.XPATH,
            "//div[@class='displayElementText RESOURCE_NAME']")
        print ("Resource Name: %s" % resource_name[record_index].text)

        ###########################
        # METADATA
        ###########################

        # Asset Name
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText ASSET_NAME']
        asset_name = record.find_elements(By.XPATH,
            "//div[@class='displayElementText ASSET_NAME']")
        print ("Asset Name: %s" % asset_name[record_index].text)

        # File Size
        #//div[@class='properties']//div[@class='displayElementText FILE_SIZE']
        file_size = record.find_elements(By.XPATH,
            "//div[@class='properties']//div[@class='displayElementText FILE_SIZE']")
        print ("File Size: %s" % file_size[record_index].text)

        # Title
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText TITLE']
        title = record.find_elements(By.XPATH,
            "//div[@class='displayElementText TITLE']")
        print ("Title: %s" % title[record_index].text)

        # Description
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText DESCRIPTION']
        description = record.find_elements(By.XPATH,
            "//div[@class='displayElementText DESCRIPTION']")
        print ("Description: %s" % description[record_index].text)

        # Contributor
        #//div[@class='displayElementText CONTRIBUTOR']
        contributor = record.find_elements(By.XPATH,
            "//div[@class='displayElementText CONTRIBUTOR']")
        length = len(contributor) - 1
        if (length > -1):
            if (contributor[length].text):
                print ("Contributor: %s" % contributor[length].text)

        # TODO: FIX THIS
        # Type
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText RESOURCE_TYPE']
        type = record.find_elements(By.XPATH,
            "//div[@class='displayElementText RESOURCE_TYPE']")
        print ("Type: ->%s<-" % type[record_index].text)

        # Digital Format
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText DIGITAL_FORMAT']
        digital_format = record.find_elements(By.XPATH,
            "//div[@class='displayElementText DIGITAL_FORMAT']")
        print ("Digital Format: %s" % digital_format[record_index].text)

        # URL for File
        #//div[@id='detail_biblio6']//div//a[@title='External Link to Asset']
        # Oops, I used driver instead of record; but it works so leave it, future TODO
        url_for_file = driver.find_elements_by_partial_link_text('sanle')
        print ("URL for File: %s" % url_for_file[record_index].text)
        print ("\n----")

        # TODO: PRINT ALL DATA TO A .CSV FILE
        # Save the scraped info to a file
        # with open('records.csv', 'a') as f:
        #     for i in range(len(links)):
        #         print (links[i].text)
        #         f.write ((links[i].text) + "\n")


        # Locate the white sub-page close button and click it.
        # Notice 'count', because each sub-page close button is unique!
        close_button = record.find_element(By.XPATH, "//div[@class='ui-dialog ui-widget ui-widget-content ui-corner-all detailModalDialog detailDialog" + str(count) + "']//span[@class='ui-icon ui-icon-closethick'][contains(text(),'close')]")
        close_button.click()
        count += 1
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

# Comparison of two links for each record in search results; both links lead to same, detailed sub-page.
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

# 110.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true&rw=108#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f7428/1/1/9?rw=108&te=ASSET&isd=true

# 2526.
# https://sanle.ent.sirsi.net/client/en_US/default/search/results?rw=2520&te=ASSET&isd=true#
# https://sanle.ent.sirsi.net/client/en_US/default/search/results.displaypanel.displaycell.detailclick/ent:$002f$002fSD_ASSET$002f0$002f6409/5/5/210?rw=2520&te=ASSET&isd=true



import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# All fields for a single record
class CSVrecord(object):
    def __init__(self):
        self.resource_name = None
        self.asset_name = None
        self.file_size = None
        self.title = None
        self.description = None
        self.contributor = None
        self.digital_format = None
        self.url_for_file = None

# We will augment this URL to navigate to successive search pages
baseURL = "https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true"
# Open Chrome
driver = webdriver.Chrome()

# Create output .csv file
with open('SLHPA-records.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow([
        'resource_name',
        'asset_name',
        'file_size',
        'title',
        'description',
        'contributor',
        'digital_format',
        'url_for_file',
    ])

# Used to identify close button on sub-pages
# 2526 records total, numbered 0 through 2525.
count = 2520    # last page
count = 2508    # 2nd to last page
count = 108     # problematic record 110.
count = 2496    # 3rd to last page
count = 0       # begin at beginning

# Iterate over all search pages
#for page in range (count, 2521, 12):       # all pages
#for page in range (count, 12, 12):         # first page only
#for page in range (count, 2521, 12):       # last page only
#for page in range (count, 2521, 12):       # last two pages only
#for page in range (count, 25, 12):         # first three pages
#for page in range (count, 108+12, 12):       # begin page ten, record 109. **THE BUG IS RECORD 110.**
#for page in range (count, 2521, 12):       # last three pages only; first record here showed BUG
for page in range (count, 2521, 12):       # all pages

    # Open URL for this search page
    driver.get(baseURL + '&rw=' + str(page))

    # This XPath returns an iterable list of records found on this search page
    list_of_records = driver.find_elements(By.XPATH, "//div[contains(@id,'syndeticsImg')]")


    # All search pages return 12 records; except the last page, which has only 6 records
    #for record_index in range(0, 2, 1):    # only look at first few records
    for record_index in range(0, len(list_of_records), 1):

        # Class to hold a record
        this_record = CSVrecord()

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
        this_record.resource_name = resource_name[record_index].text

        ###########################
        # METADATA
        ###########################

        # Asset Name
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText ASSET_NAME']
        asset_name = record.find_elements(By.XPATH,
            "//div[@class='displayElementText ASSET_NAME']")
        print ("Asset Name: %s" % asset_name[record_index].text)
        this_record.asset_name = asset_name[record_index].text

        # File Size
        #//div[@class='properties']//div[@class='displayElementText FILE_SIZE']
        file_size = record.find_elements(By.XPATH,
            "//div[@class='properties']//div[@class='displayElementText FILE_SIZE']")
        print ("File Size: %s" % file_size[record_index].text)
        this_record.file_size = file_size[record_index].text

        # Title
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText TITLE']
        title = record.find_elements(By.XPATH,
            "//div[@class='displayElementText TITLE']")
        print ("Title: %s" % title[record_index].text)
        this_record.title = title[record_index].text

        # Description
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText DESCRIPTION']
        description = record.find_elements(By.XPATH,
            "//div[@class='displayElementText DESCRIPTION']")
        print ("Description: %s" % description[record_index].text)
        this_record.description = description[record_index].text

        # Contributor
        #//div[@class='displayElementText CONTRIBUTOR']
        contributor_field = None
        contributor = record.find_elements(By.XPATH,
            "//div[@class='displayElementText CONTRIBUTOR']")
        last_element = len(contributor) - 1
        if (last_element > -1):
            if (contributor[last_element].text):
                print ("Contributor: %s" % contributor[last_element].text)
                this_record.contributor = contributor[last_element].text
        # # A better equivalent?
        # if (contributor):
        #     print ("Contributor: %s" % contributor[-1].text)

        # # TODO: FIX THIS
        # # Type
        # #//div[@id='detail_biblio6']//div//div[@class='displayElementText RESOURCE_TYPE']
        # type = record.find_elements(By.XPATH,
        #     "//div[@class='displayElementText RESOURCE_TYPE']")
        # print ("Type: ->%s<-" % type[record_index].text)

        # Digital Format
        #//div[@id='detail_biblio6']//div//div[@class='displayElementText DIGITAL_FORMAT']
        digital_format = record.find_elements(By.XPATH,
            "//div[@class='displayElementText DIGITAL_FORMAT']")
        print ("Digital Format: %s" % digital_format[record_index].text)
        this_record.digital_format = digital_format[record_index].text

        # URL for File
        #//div[@id='detail_biblio6']//div//a[@title='External Link to Asset']
        # Oops, I used driver instead of record; but it works so leave it, future TODO
        url_for_file = driver.find_elements_by_partial_link_text('sanle')
        print ("URL for File: %s" % url_for_file[record_index].text)
        this_record.url_for_file = url_for_file[record_index].text
        print ("\n----")

        # Locate the white sub-page close button and click it.
        # Notice 'count', because each sub-page close button is unique!
        close_button = record.find_element(By.XPATH, "//div[@class='ui-dialog ui-widget ui-widget-content ui-corner-all detailModalDialog detailDialog" + str(count) + "']//span[@class='ui-icon ui-icon-closethick'][contains(text(),'close')]")
        close_button.click()
        count += 1
        time.sleep(1)

        # Append this record to output .csv file
        # https://docs.python.org/3/library/csv.html
        with open('SLHPA-records.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([
                this_record.resource_name,
                this_record.asset_name,
                this_record.file_size,
                this_record.title,
                this_record.description,
                this_record.contributor,
                this_record.digital_format,
                this_record.url_for_file,
            ])

# Rename output .csv file so it won't get clobbered next run
os.rename('SLHPA-records.csv', 'SLHPA-records_' + time.strftime("%Y%m%d-%H%M%S") + '.csv')
# Close the selenium webdriver
driver.close()


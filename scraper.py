import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import os
import sys
import datetime
from dumper import dump


# All fields for a single record
class CSVrecord(object):
    def __init__(self):
        self.resource_name = None
        self.asset_name = None
        self.file_size = None
        self.title = None
        self.subject = None
        self.description = None
        self.contributor = None
        self.digital_format = None
        self.url_for_file = None


def badValue(theArray, theIndex):
    if (not theArray):
        return True
    if (theIndex >= len(theArray)):
        return True
    if (not theArray[theIndex].text):
        return True
    return False


def close(record, count):
    # Locate the white sub-page close button and click it.
    # Notice 'count', because each sub-page close button is unique!
    close_button = record.find_element(By.XPATH, "//div[@class='ui-dialog ui-widget ui-widget-content ui-corner-all detailModalDialog detailDialog" + str(count) + "']//span[@class='ui-icon ui-icon-closethick'][contains(text(),'close')]")
    close_button.click()
    time.sleep(3)


def add_skipped_record(record_index, page_number, absolute_record_number, skipped_pages):
    errorFormat = "Failed to get resource_name for record : {} on page: {} ({}). Skipping record."
    err = errorFormat.format(record_index, int(page_number), absolute_record_number)
    log(err)
    skipped_pages.append(err)


def scan_pages(driver, more_pages, skipped_pages):
    page_to_start_on = more_pages[0]
    page_to_end_on = int(2526 / 12)    # 2526 records total, 12 per page
    if (len(more_pages) > 1):
        page_to_end_on = more_pages[1]

    count = (page_to_start_on - 1) * 12
    absolute_record_number = count + 1
    next_pages = []

    wait = WebDriverWait(driver, 10, poll_frequency=1,
        ignored_exceptions=[NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException])

    for page in range (count, (page_to_end_on * 12) + 1, 12):

        # Open URL for this search page
        page_number = int(page / 12 + 1)
        try:
            driver.get(baseURL + '&rw=' + str(page))
            print(" %i" % page, end = "")

            # This XPath returns an iterable list of records found on this search page
            list_of_records = driver.find_elements(By.XPATH, "//div[contains(@id,'syndeticsImg')]")

            # All search pages return 12 records except the last page, which has only 6 records.
            # Most DOM selectors use .find_elements, plural, which returns an array of values.
            #for record_index in range(0, 2, 1):    # only look at first few records
            for record_index in range(0, len(list_of_records), 1):

                # Class to hold a record
                this_record = CSVrecord()

                # Open the white sub-page for this record
                # log("record_index: " + str(record_index))
                # log("absolute_record_number: " + str(absolute_record_number))
                record = list_of_records[record_index]
                record.click()
                time.sleep(1)

                # Resource Name
                # We do an explit wait on this find command, because Resource Name is the first
                # element on the page.
                for i in range (0, 10):
                    resource_name = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                        "//div[@class='displayElementText RESOURCE_NAME']")))
                    if (resource_name):
                        break
                if (badValue(resource_name, record_index)):
                    add_skipped_record(record_index, page_number, absolute_record_number, skipped_pages)
                    close(record, count)
                    count += 1
                    absolute_record_number = absolute_record_number + 1
                    next_pages.append(page_number)
                    return next_pages
                this_record.resource_name = resource_name[record_index].text

                # Asset Name
                asset_name = record.find_elements(By.XPATH,
                    "//div[@class='displayElementText ASSET_NAME']")
                if (not badValue(asset_name, record_index)):
                    this_record.asset_name = asset_name[record_index].text

                # File Size
                file_size = record.find_elements(By.XPATH,
                    "//div[@class='properties']//div[@class='displayElementText FILE_SIZE']")
                if (not badValue(file_size, record_index)):
                    this_record.file_size = file_size[record_index].text

                # Title
                title = record.find_elements(By.XPATH,
                    "//div[@class='displayElementText TITLE']")
                if (not badValue(title, record_index)):
                    this_record.title = title[record_index].text

                # TODO: fix this
                # Subject
                #//div[@class='displayElementLabel SUBJECT_label']//div[@class='displayElementText']//table
                # subject = record.find_elements(By.XPATH,
                #     "//div[@class='displayElementText']//table/tbody/tr")
                # if (subject):
                #     rows = subject.find_elements(By.TAG_NAME, 'tr')
                this_record.subject = ''

                # TODO: fix this
                # Description
                description = record.find_elements(By.XPATH,
                    "//div[@class='displayElementText DESCRIPTION']")
                if (not badValue(description, record_index)):
                    this_record.description = description[record_index].text

                # Contributor
                contributor_field = None
                contributor = record.find_elements(By.XPATH,
                    "//div[@class='displayElementText CONTRIBUTOR']")
                last_element = len(contributor) - 1
                if (last_element > -1):
                    if (contributor[last_element].text):
                        this_record.contributor = contributor[last_element].text

                # Digital Format
                digital_format = record.find_elements(By.XPATH,
                    "//div[@class='displayElementText DIGITAL_FORMAT']")
                if (not badValue(digital_format, record_index)):
                    this_record.digital_format = digital_format[record_index].text

                # URL for File
                # Oops, I used driver instead of record; but it works so leave it, future TODO
                url_for_file = driver.find_elements_by_partial_link_text('sanle')
                if (badValue(url_for_file, record_index)):
                    add_skipped_record(record_index, page_number, absolute_record_number, skipped_pages)
                    close(record, count)
                    count += 1
                    absolute_record_number = absolute_record_number + 1
                    next_pages.append(page_number)
                    return next_pages

                this_record.url_for_file = url_for_file[record_index].text

                close(record, count)
                count += 1
                absolute_record_number = absolute_record_number + 1

                # Append this record to output .csv file
                # https://docs.python.org/3/library/csv.html
                with open('SLHPA-records.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([
                        this_record.resource_name,
                        this_record.asset_name,
                        this_record.file_size,
                        this_record.title,
                        this_record.subject,
                        this_record.description,
                        this_record.contributor,
                        this_record.digital_format,
                        this_record.url_for_file,
                    ])
                print(".", end = "")
        except:
            return [page_number]
    return []


def scan(more_pages):
    next_pages = []
    skipped_records = [];

    # Open Chrome
    driver = webdriver.Chrome()
    # Implicit wait - tells web driver to poll the DOM for specified time; wait is set for duration of web driver object
    driver.implicitly_wait(2)

    # Create output .csv file
    with open('SLHPA-records.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'resource_name',
            'asset_name',
            'file_size',
            'title',
            'subject',
            'description',
            'contributor',
            'digital_format',
            'url_for_file',
        ])

    try:
        next_pages = scan_pages(driver, more_pages, skipped_records)
    except:
        log("Caught exception in scan(): " + str(sys.exc_info()[0]))

    for s in skipped_records:
        log(s)

    # Rename output .csv file so it won't get clobbered next run
    os.rename('SLHPA-records.csv', 'SLHPA-records_' + time.strftime("%Y%m%d-%H%M%S") + '.csv')
    # Close the selenium webdriver
    driver.close()
    return next_pages


def log(message):
    print(str(datetime.datetime.now()) + '\t' + message)


# We will augment this URL to navigate to successive search pages
baseURL = "https://sanle.ent.sirsi.net/client/en_US/default/search/results?te=ASSET&isd=true"
starttime = datetime.datetime.now()
log("Started scraping")
try:
    more_pages = [1]
    while (len(more_pages) > 0):
        log("starting at page: " + str(more_pages[0]))
        more_pages = scan(more_pages)
except:
    log("Caught exception in 'main': " + str(sys.exc_info()[0]))

print('')
minutes = (datetime.datetime.now() - starttime).seconds / 60
log("Elapsed minutes : " + str(int(minutes)))

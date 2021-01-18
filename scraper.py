import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import os
import sys
import datetime
import re


# All fields for a single record
class CSVrecord(object):
    def __init__(self):
        self.resource_name = ''
        self.asset_name = ''
        self.file_size = ''
        self.title = ''
        self.subject = ''
        self.description = ''
        self.contributor = ''
        self.period_date = ''
        self.digital_format = ''
        self.url_for_file = ''


def close(record, count, driver):
    """
    Close the modal popover.
    """

    close_via_escape = 1
    if (close_via_escape):
        # Send escape key, which closes the modal popover.
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    else:
        # This method is deprecated because of server-side changes that broke this locator.
        # Notice 'count', because each sub-page close button is unique!
        close_button = record.find_element(By.XPATH, "//div[@class='ui-dialog ui-widget ui-widget-content ui-corner-all detailModalDialog detailDialog" + str(
            count) + "']//span[@class='ui-icon ui-icon-closethick'][contains(text(),'close')]")
        close_button.click()
    time.sleep(3)


def add_skipped_record(record_index, page_number, absolute_record_number, skipped_pages):
    errorFormat = "Failed to get resource_name for record: {} on page: {} ({}). Retrying page."
    err = errorFormat.format(record_index, int(
        page_number), absolute_record_number)
    log('\n' + err)
    skipped_pages.append(err)


def is_bad_value(the_array, the_index):
    if (not the_array):
        #print ('EmptyArray!', end='')
        return True
    if (the_index >= len(the_array)):
        #print ('IndexRangeErr!', end='')
        return True
    if (not the_array[the_index].text):
        #print ('NoText!', end='')
        return True
    return False


def scan_pages(driver, more_pages, skipped_pages):
    page_to_start_on = more_pages[0]
    page_to_end_on = int(2526 / 12)    # 2526 records total, 12 per page
    if (len(more_pages) > 1):
        page_to_end_on = more_pages[1]

    count = (page_to_start_on - 1) * 12
    absolute_record_number = count + 1
    next_pages = []

    # Explicit wait
    wait = WebDriverWait(driver, 10, poll_frequency=1,
                         ignored_exceptions=[NoSuchElementException,
                                             ElementNotVisibleException,
                                             ElementNotSelectableException])

    for search_page_num in range(count, (page_to_end_on * 12) + 1, 12):

        page_number = int(search_page_num / 12 + 1)
        try:
            # Open URL for this search page
            driver.get(baseURL + '&rw=' + str(search_page_num))
            print(" %i" % search_page_num, end='')

            # This XPath returns an iterable list of records found on this search page
            list_of_records = driver.find_elements(
                By.XPATH, "//div[contains(@id,'syndeticsImg')]")

            # Special index variables for subject and description fields (in lieu of record_index),
            # because records can have more than 1 of these types of elements.
            subj_index = 0
            desc_index = 0

            # All search pages return 12 records except the last page, which has only 6 records.
            # Most locators use .find_elements, plural, which returns an array.
            for record_index in range(0, len(list_of_records), 1):

                # Class to hold a record
                this_record = CSVrecord()

                # Open the modal popover for this record
                record = list_of_records[record_index]
                record.click()
                time.sleep(1)

                common_classes = 'displayElementText text-p'
                # Resource Name
                resource_name = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                            "//div[@class='" + common_classes + " RESOURCE_NAME']")))
                if (is_bad_value(resource_name, record_index)):
                    add_skipped_record(
                        record_index, page_number, absolute_record_number, skipped_pages)
                    close(record, count, driver)
                    count += 1
                    absolute_record_number = absolute_record_number + 1
                    next_pages.append(page_number)
                    return next_pages
                this_record.resource_name = resource_name[record_index].text

                # Asset Name
                asset_name = record.find_elements(By.XPATH,
                        "//div[@class='" + common_classes + " ASSET_NAME']")
                if (not is_bad_value(asset_name, record_index)):
                    this_record.asset_name = asset_name[record_index].text

                # File Size
                file_size = record.find_elements(By.XPATH,
                        "//div[@class='properties']//div[@class='" + common_classes + " FILE_SIZE']")
                if (not is_bad_value(file_size, record_index)):
                    this_record.file_size = file_size[record_index].text

                # Title
                title = record.find_elements(By.XPATH,
                                             "//div[@class='" + common_classes + " TITLE']")
                if (not is_bad_value(title, record_index)):
                    this_record.title = title[record_index].text

                # Subject
                # Field may or may not be defined; if defined, may contain more than 1 table data rows
                subject = record.find_elements(By.XPATH,
                        "//div[@class='detail_biblio resource_margin']//table//td")
                if (not is_bad_value(subject, subj_index)):
                    this_record.subject = '| '
                    for i in range(subj_index, len(subject), 1):
                        this_record.subject += subject[i].text + ' | '
                    this_record.subject = this_record.subject.rstrip()
                    subj_index = len(subject)

                # Description
                # Field is always defined, but may contain more than 1 description elements
                description = record.find_elements(By.XPATH,
                        "//div[@class='" + common_classes + " DESCRIPTION']")
                if (not is_bad_value(description, desc_index)):
                    for i in range(desc_index, len(description), 1):
                        # Deal with punctuation at end of string(s)
                        if (re.findall(r'[\.\?\!\,\'\"][\"\'\)\s]*$', description[i].text)):
                            this_record.description += description[i].text + ' '
                        else:
                            this_record.description += description[i].text + '. '
                    this_record.description = this_record.description.rstrip()
                    desc_index = len(description)

                # Contributor
                # Field may or may not be defined; if defined, will only contain 1 contributor element
                contributor = record.find_elements(By.XPATH,
                        "//div[@class='" + common_classes + " CONTRIBUTOR']")
                if (len(contributor)):
                    this_record.contributor = contributor[-1].text

                # Period Date
                # Field may or may not be defined; if defined, will only contain 1 period_date element
                period_date = record.find_elements(By.XPATH,
                        "//div[@class='" + common_classes + " PERIOD_DATE']")
                if (len(period_date)):
                    this_record.period_date = period_date[-1].text

                # Digital Format
                digital_format = record.find_elements(By.XPATH,
                        "//div[@class='" + common_classes + " DIGITAL_FORMAT']")
                if (not is_bad_value(digital_format, record_index)):
                    this_record.digital_format = digital_format[record_index].text

                # URL for File
                url_for_file = driver.find_elements_by_partial_link_text(
                    'sanle')
                if (is_bad_value(url_for_file, record_index)):
                    add_skipped_record(
                        record_index, page_number, absolute_record_number, skipped_pages)
                    close(record, count, driver)
                    count += 1
                    absolute_record_number = absolute_record_number + 1
                    next_pages.append(page_number)
                    return next_pages
                this_record.url_for_file = url_for_file[record_index].text

                close(record, count, driver)
                count += 1
                absolute_record_number = absolute_record_number + 1

                # Append this record to output .csv file
                # https://docs.python.org/3/library/csv.html
                with open('SLHPA-records.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(
                        csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow([
                        this_record.resource_name,
                        this_record.asset_name,
                        this_record.file_size,
                        this_record.title,
                        this_record.subject,
                        this_record.description,
                        this_record.contributor,
                        this_record.period_date,
                        this_record.digital_format,
                        this_record.url_for_file,
                    ])
                print('.', end='', flush=True)
        except:
            return [page_number]
    return []


def scan(more_pages):
    next_pages = []
    skipped_records = []

    # Open browser
    driver = None
    try:
        driver = webdriver.Chrome()
    except:
        driver = webdriver.Firefox()

    # Implicit wait - tells web driver to poll the DOM for specified time;
    # wait is set for duration of web driver object.
    driver.implicitly_wait(2)

    # Create output .csv file
    with open('SLHPA-records.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'resource_name',
            'asset_name',
            'file_size',
            'title',
            'subject',
            'description',
            'contributor',
            'period_date',
            'digital_format',
            'url_for_file',
        ])

    try:
        next_pages = scan_pages(driver, more_pages, skipped_records)
    except:
        log("Caught exception in scan(): " + str(sys.exc_info()[0]))

    # Rename output .csv file so it won't get clobbered next run
    os.rename('SLHPA-records.csv', 'SLHPA-records_' +
              time.strftime("%Y%m%d-%H%M%S") + '.csv')
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
except Exception as e:
    log("Caught exception in 'main': " + str(e))

print('')
minutes = (datetime.datetime.now() - starttime).seconds / 60
log("Elapsed minutes: " + str(int(minutes)))

# SLHPA-Web-App
San Leandro Historical Photo Archive Web Application

![San Leandro](https://images-na.ssl-images-amazon.com/images/I/51A-MaecjhL.jpg)

# Contents
1. [Overview](#overview)
2. [Setup](#Setup)
      1. [Python Dependencies](#python-dependencies)
3. [How to Deploy to GCP](#how-to-deploy-to-gcp)
4. [Data Gathering Tools](#data-gathering-tools)
      1. [scraper](#scraper)
      2. [merger](#merger)
      3. [transformer](#transformer)
      4. [mapper](#mapper)
      5. [Run pipeline](#run-pipeline)
5. [Web Application](#web-application)

## Overview

The San Leandro Public Library is home to an archive of about 2500 photographic prints related to the history of San Leandro. These prints have also been scanned, and are accessible online through the library's Catalog Search, available at http://sanleandro.org/depts/library/default.asp

This SLHPA-Web-App project is an attempt to make the historical photo archive more easily browsable, by creating a historical photo website that uses dynamic elements such as user-customizable filter settings, photo carousel, or maps/markers.

## Setup

See https://github.com/jeffb4real/SLHPA-Web-App/blob/master/utilities/bootstrap.sh for a shell script to do most of the bootstrapping.

### Python Dependencies

This project was created with Python 3.7.x, with the addition of these modules:

* [selenium](https://seleniumhq.github.io/selenium/docs/api/py/api.html) - used by `scraper.py` to scrape photo data
* [lxml](https://lxml.de/) - used by `mapper.py` to write KML data
* [Django](https://docs.djangoproject.com/en/2.1/) - used by slhpa web app
* [django-tables2](https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html) - used by slhpa web app
* [django-filter](https://django-filter.readthedocs.io/en/master/) - used by slhpa web app
* [django-bootstrap3](https://django-bootstrap3.readthedocs.io/en/latest/) - used by slhpa web app

These modules can be installed all at once either by using `bootstrap.sh` (mentioned above) or by `pip` installing the included requirements.txt, e.g.:

            ~/SLHPA-Web-App $ pip install -r mysite/requirements.txt

## How to setup development environment and deploy to GCP

Google Document : https://docs.google.com/document/d/1WW6QUk7ubjsIsqsXWsqNYTzdCQECn5WDYyMCx_yHL1Q/edit

## Data Gathering Tools

_Note: In all examples, `python` refers to `python3`._

### scraper

This Python script uses Selenium (https://www.seleniumhq.org/) to "scrape" metadata from the online photo archive. This script technically needs to work correctly just once, as the photo archive is a dead database and will never be updated.

`scraper.py` collects publicly available information about the online photo archive. For each photograpic record, this includes collecting: the title, description, and contributor of the photo, where available, as well as the web URL and file size of the photographic document (*.pdf).

`scraper.py` then stores all the collected information in a database of records (.csv file, for now), which ultimately will be used by the SLHPA web application.

#### How To Run `scraper.py`

1. Install Python (3.7.0 or later).

2. Set up your Python environment.

   To install the required module:
   
            $ pip install selenium
    
   This Python script was run using `selenium 3.14.1`.
   
3. Download the Selenium chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads

4. Unzip chromedriver and add its location to your `PATH`.

5. Open `cmd.exe` (Windows) or Terminal (MacOS).

6. `cd` into the directory where you keep your Github repository directories.

7. Clone this project:

            $ git clone https://github.com/jeffb4real/SLHPA-Web-App.git
    
8. Navigate to the repository directory:

            $ cd SLHPA-Web-App

9. Run the script:

            $ python scraper.py

### Merger

This Python script performs data cleaning/augmentation on the scraped data. Input to this script is the .csv file produced by running `scraper.py`. Output from this script is a .csv file containing a version of the data modified in the following ways:

* Remove meaningless "Vol. xx" entries from `description` field. This type of entry is a reference to non-existent paper volumes, deprecated many years ago.

* Populate the `date` field, if a valid year (see below) can be found within the title, subject, or description fields. This script is not infallible; but it will likely pick the correct year when one is listed, and will ultimately save a lot of manual data entry. However, the output .csv file must be manually verified for correctness.

   A valid year is one between 1839 (the invention of photography) and 1980 (approximate culmination of the photo archive). When multiple years are found, the highest year will be used. For example, for this description:

            St. Leander's Rectory, 1899-1949, razed in 1954 photo taken around 1914.
   
`merger.py` will find a list of years, [1899, 1949, 1954, 1914], and return 1954. This is a good example of why the `date` field will need to be manually verified in the output .csv file.

* Merge description information contained in a .xls file on a DVD version of the photo archive, produced around 2003. A new field, `description_from_DVD`, is inserted next to the existing `description` field, and is populated only when the description field from the DVD adds new information.

#### How to run `merger.py`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

            $ cd SLHPA-Web-App

2. Run the script:

            $ python merger.py

### transformer

Python script to convert legacy photo location coordinates into coordinates compatible with modern online map hosts.

Input is a .csv file. Output is a .csv file.

#### How to run `transformer.py`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

            $ cd SLHPA-Web-App

2. Run the script:

            $ python transformer.py

### mapper

Python script to convert photo location coordinates into [KML](#https://en.wikipedia.org/wiki/Keyhole_Markup_Language) that can be imported into map host.

Input is a .csv file. Output is a .kml file (additional .kml output files for debug purposes only).

#### How to run `mapper.py`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

            $ cd SLHPA-Web-App

2. Run the script:

            $ python mapper.py

### Run pipeline

This is a BASH script that serially runs all of the above tools, except scraper.py.

#### How to run `run-pipeline.sh`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

            $ cd SLHPA-Web-App

2. Run the script:

            $ ./run-pipeline.sh

## Web Application

See https://github.com/jeffb4real/SLHPA-Web-App/blob/master/utilities/bootstrap.sh

## Automated tests

https://github.com/chrisxkeith/slhpa-web-app-test

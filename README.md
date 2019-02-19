# SLHPA-Web-App
San Leandro Historical Photo Archive Web Application

![San Leandro](https://images-na.ssl-images-amazon.com/images/I/51A-MaecjhL.jpg)

# Contents
1. [Overview](#overview)
2. [Python_Dependencies](#Python_Dependencies)
3. [scraper](#scraper)
4. [merger](#merger)
5. [transformer](#transformer)
6. [mapper](#mapper)
7. [run-pipeline](#run-pipeline)
8. [Web_Application](#Web_Application)

## Overview

The San Leandro Public Library is home to an archive of about 2500 photographic prints related to the history of San Leandro. These prints have also been scanned, and are accessible online through the library's Catalog Search, available at http://sanleandro.org/depts/library/default.asp

This SLHPA-Web-App project is an attempt to make the historical photo archive more easily browsable, by creating a historical photo website that uses dynamic elements such as user-customizable filter settings, photo carousel, or maps/markers.

## Python_Dependencies

This project was created with Python 3.7.x, with the addition of these modules:

* selenium - used by `scraper.py` to scrape photo data
* lxml - used by `mapper.py` to write KML data
* django_tables2 - used by "mysite/tutorial" app (https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html)

These modules were installed with pip, e.g.:

      $ python -m pip install selenium

## scraper

This Python script uses Selenium (https://www.seleniumhq.org/) to "scrape" metadata from the online photo archive. This script technically needs to work correctly just once, as the photo archive is a dead database and will never be updated.

`scraper.py` collects publicly available information about the online photo archive. For each photograpic record, this includes collecting: the title, description, and contributor of the photo, where available, as well as the web URL and file size of the photographic document (*.pdf).

`scraper.py` then stores all the collected information in a database of records (.csv file, for now), which ultimately will be used by the SLHPA web application.

### How To Run `scraper.py`

1. Install Python (3.7.0 or later).

2. Set up your Python environment.

   To install the required module:
   
    $ pip install selenium
    
   This Python script was run using `selenium 3.14.1`.
   
3. Download the Selenium chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads

4. Unzip chromedriver and add its location to your `PATH`.

5. Open `cmd.exe` (Windows) or Terminal (MacOS).

6. 'cd' into the diretory where you keep your Github repository directories.

7. Clone this project:

    $ git clone https://github.com/jeffb4real/SLHPA-Web-App.git
    
8. Navigate to the repository directory:

    $ cd SLHPA-Web-App

9. Run the script:

    $ python scraper.py

## Merger

This Python script performs data cleaning/augmentation on the scraped data. Input to this script is the .csv file produced by running `scraper.py`. Output from this script is a .csv file containing a version of the data modified in the following ways:

* Remove meaningless "Vol. xx" entries from `description` field. This type of entry is a reference to non-existent paper volumes, deprecated many years ago.

* Populate the `date` field, if a valid year (see below) can be found within the title, subject, or description fields. This script is not infallible; but it will likely pick the correct year when one is listed, and will ultimately save a lot of manual data entry. However, the output .csv file must be manually verified for correctness.

   A valid year is one between 1839 (the invention of photography) and 1980 (approximate culmination of the photo archive). When multiple years are found, the highest year will be used. For example, for this description:

      St. Leander's Rectory, 1899-1949, razed in 1954 photo taken around 1914.
   
   `merger.py` will find a list of years, [1899, 1949, 1954, 1914], and return 1954. This is a good example of why the `date` field will need to be manually verified in the output .csv file.

* Merge description information contained in a .xls file on a DVD version of the photo archive, produced around 2003. A new field, `description_from_DVD`, is inserted next to the existing `description` field, and is populated only when the description field from the DVD adds new information.

### How to run `merger.py`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

      $ cd SLHPA-Web-App

2. Run the script:

      $ python merger.py

## transformer

Python script to convert legacy photo location coordinates into coordinates compatible with modern online map hosts.

Input is a .csv file. Output is a .csv file.

### How to run `transformer.py`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

      $ cd SLHPA-Web-App

2. Run the script:

      $ python transformer.py

## mapper

Python script to convert photo location coordinates into [KML](#https://en.wikipedia.org/wiki/Keyhole_Markup_Language) that can be imported into map host.

Input is a .csv file. Output is a .kml file (additional .kml output files for debug purposes only).

### How to run `mapper.py`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

      $ cd SLHPA-Web-App

2. Run the script:

      $ python mapper.py

## run-pipeline

This is a simple BASH script that serially runs all of the above tools, except scraper.py.

### How to run `run-pipeline.sh`

Assuming this project has already been cloned:

1. Navigate to the repository directory:

      $ cd SLHPA-Web-App

2. Run the script:

      $ ./run-pipeline.sh

## Web_Application

(... documentation in process)

* Bootstrap
* Some map host:
   [The Top 10 Mapping & Maps APIs (for Developers in 2018)](https://blog.rapidapi.com/top-map-apis/)
  1. Mapbox
  2. Google maps
  3. [folium](https://pypi.org/project/folium/): "Make beautiful, interactive maps with Python and Leaflet.js"
  4. [Leaflet API](https://leafletjs.com/)
  5. [Open Street Map](https://switch2osm.org/)
  6. [Mapfit](https://www.mapfit.com/developers)

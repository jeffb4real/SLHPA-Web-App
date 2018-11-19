# SLHPA-Web-App
San Leandro Historical Photo Archive Web Application

# Contents
1. [Overview](#overview)
2. [scraper](#scraper)
3. [Web_Application](#Web_Application)

## Overview

The San Leandro Public Library is home to an archive of about 2500 photographic prints related to the history of San Leandro. These prints have also been scanned, and are accessible through the library's Catalog Search, available at http://sanleandro.org/depts/library/default.asp

This SLHPA-Web-App project is an attempt to make the photo archive more easily accessible. 

## scraper

This is a Python script that only needs to run correctly once, and then it's end-of-life. The online photo archive is a dead database, and will never be updated.

scraper.py collects all the public, web-available information about the online photo archive. For each photograpic record, this includes collecting: the title, description, and contributor of the photo, where available, as well as the web URL and file size of the photographic document.

scraper.py then stores all the collected information in a database (.csv file, for now), which ultimately will reside in the web application.

### How To Run scraper.py

1. Install Python (3.7.0 or later).

2. Set up your Python environment:

   To install modules in Python:
   
    $ pip install selenium
    
   This Python script was run using selenium 3.14.1.
   
3. Download the Selenium chromedriver from https://sites.google.com/a/chromium.org/chromedriver/downloads

4. Unzip chromedriver.exe and add its location to your path.

5. Open cmd.exe (Windows) or Terminal (MacOS)

6. 'cd' into the diretory where you keep your Github repository directories.

7. Clone this project:

    $ git clone https://github.com/jeffb4real/SLHPA-Web-App.git
    
8. 'cd' into the repository directory:

    $ cd SLHPA-Web-App

9. Run the scraper:

    $ python scraper.py

## Web_Application (... documentation in process)

* Bootstrap
* Some Python-compatible map host: https://blog.rapidapi.com/top-map-apis/
  1. Mapbox
  2. Google maps
  3. folium: https://pypi.org/project/folium/

# Do everything to set up data scraping, creating KML files and running Django.

set -x

cd ~/Documents/Github/SLHPA-Web-App                     ; if [ $? -ne 0 ] ; then exit -6 ; fi
virtualenv venv                                         ; if [ $? -ne 0 ] ; then exit -6 ; fi
venv/Scripts/activate                                   ; if [ $? -ne 0 ] ; then exit -6 ; fi

python -m pip install selenium                          ; if [ $? -ne 0 ] ; then exit -6 ; fi
python -m pip install lxml                              ; if [ $? -ne 0 ] ; then exit -6 ; fi

echo "To verify that web scraping works, run:"
echo "python scraper.py"

./run-pipeline.sh                                       ; if [ $? -ne 0 ] ; then exit -6 ; fi

python -m pip install django                            ; if [ $? -ne 0 ] ; then exit -6 ; fi
python -m pip install django-tables2                    ; if [ $? -ne 0 ] ; then exit -6 ; fi
cd mysite                                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py migrate                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py runserver                              ; if [ $? -ne 0 ] ; then exit -6 ; fi

echo "Example command line to copy image files. They must be correctly distributed into numbered subdirectories."
echo "cp -r ~/Downloads/'San Leandro Historical Photo Archive - 311MB/photos - 640x only'/* slhpa/static/slhpa/images/photos/"

echo "Use browser to import csv into sqlite with this URL:"
echo "http://127.0.0.1:8000/slhpa/import/transformed"
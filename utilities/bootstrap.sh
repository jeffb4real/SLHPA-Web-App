# Do everything to set up data scraping, creating KML files and running Django.

set -x

if [ ! "$WINDIR" = "" ] ; then
    echo "Do not run on Windows. Use CMD instead."
    exit -1
fi

cd ~/Documents/Github/SLHPA-Web-App                     ; if [ $? -ne 0 ] ; then exit -6 ; fi
python -m venv venv                                     ; if [ $? -ne 0 ] ; then exit -6 ; fi
source venv/bin/activate                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
pip install -r mysite/requirements.txt                  ; if [ $? -ne 0 ] ; then exit -6 ; fi

./run-pipeline.sh                                       ; if [ $? -ne 0 ] ; then exit -6 ; fi
cd mysite                                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py migrate                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py createsuperuser                        ; if [ $? -ne 0 ] ; then exit -6 ; fi

echo "Example command line to copy image files. They must be correctly distributed into numbered subdirectories."
echo "time cp -r ~/Documents/'San Leandro Historical Photo Archive - 311MB/photos - 640x only'/*  ~/Documents/Github/SLHPA-Web-App/mysite/slhpa/static/slhpa/images/photos/"

echo "Run server with: python manage.py runserver"
echo "Use browser to import csv into sqlite with this URL:"
echo "http://127.0.0.1:8000/slhpa/import/transformed"

echo "To verify that web scraping works, run:"
echo "python scraper.py"

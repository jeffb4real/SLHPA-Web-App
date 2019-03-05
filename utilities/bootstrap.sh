# Do everything to set up data scraping, creating KML files and running Django.

set -x

curdir=`pwd`
base=`basename $curdir`
if [ ! "$base" = "SLHPA-Web-App" ] ; then
    echo "Must run from within SLHPA-Web-App directory."
    exit -1
fi
python -m venv venv                                     ; if [ $? -ne 0 ] ; then exit -6 ; fi

if [ "$WINDIR" = "" ] ; then
    source venv/bin/activate                            ; if [ $? -ne 0 ] ; then exit -6 ; fi
else
    venv/Scripts/activate                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
fi

pip install -r requirements.txt                         ; if [ $? -ne 0 ] ; then exit -6 ; fi

echo "To verify that web scraping works, run:"
echo "python scraper.py"

./run-pipeline.sh                                       ; if [ $? -ne 0 ] ; then exit -6 ; fi

cd mysite                                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py migrate                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py createsuperuser                        ; if [ $? -ne 0 ] ; then exit -6 ; fi

echo "Example command line to copy image files. They must be correctly distributed into numbered subdirectories."
echo "cp -r ~/Downloads/'San Leandro Historical Photo Archive - 311MB/photos - 640x only'/* slhpa/static/slhpa/images/photos/"

echo "Use browser to import csv into sqlite with this URL:"
echo "http://127.0.0.1:8000/slhpa/import/transformed"

python manage.py runserver

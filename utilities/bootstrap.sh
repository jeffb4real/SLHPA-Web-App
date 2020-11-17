# Set up the development environment.

set -x

cd ~/Documents/Github/SLHPA-Web-App                     ; if [ $? -ne 0 ] ; then exit -6 ; fi
time python -m venv venv                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
time source venv/bin/activate                       ; if [ $? -ne 0 ] ; then exit -6 ; fi
time pip install -r mysite/requirements.txt             ; if [ $? -ne 0 ] ; then exit -6 ; fi

cd mysite                                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
time python manage.py migrate                           ; if [ $? -ne 0 ] ; then exit -6 ; fi
if [ ! "$WINDIR" = "" ] ; then
    echo "In CMD, run:"
    echo "python manage.py createsuperuser"
else
    python manage.py createsuperuser                    ; if [ $? -ne 0 ] ; then exit -6 ; fi
fi

echo "Temporarily edit mysite/mysite/settings.py as shown in GCP comments."
echo "Run server with: python manage.py runserver"
echo "Use browser to import csv into sqlite with this URL:"
echo "http://127.0.0.1:8000/slhpa/import/transformed"

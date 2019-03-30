# Deploy to Google Cloud Platform. Currently *in progress*.
set -x 

if [ "$TMP" = "" ] ; then
    echo No TMP environment variable!
    exit -1
fi

cd ~/Documents/Github/SLHPA-Web-App/mysite                                  ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f slhpa/static/slhpa/images/photos/hr/ $TMP/                            ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f slhpa/static/slhpa/images/photos/lr/ $TMP/                            ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f slhpa/static/slhpa/images/photos/mr/ $TMP/                            ; if [ $? -ne 0 ] ; then exit -6 ; fi

sed -i 's/ALLOW_EDIT = True/ALLOW_EDIT = False/' mysite/settings.py         ; if [ $? -ne 0 ] ; then exit -6 ; fi

# Do this if we can figure how how to run Django with the insecure flag in GCP.
# sed -i 's/DEBUG = True/DEBUG = False/' mysite/settings.py                 ; if [ $? -ne 0 ] ; then exit -6 ; fi

rm -rf static/                                                              ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py collectstatic                                              ; if [ $? -ne 0 ] ; then exit -6 ; fi
if [ "$WINDIR" = "" ] ; then
    gcloud app deploy                                                       ; if [ $? -ne 0 ] ; then exit -6 ; fi
else
    echo "Now run the following command in a CMD shell:"
    echo "cd Documents\Github\SLHPA-Web-App\mysite\\"
    echo "gcloud app deploy"
    read -p "Press any key to continue after deploy finishes... " -n1 -s
fi

# TODO : how to run 'python manage.py migrate' on GCP server?

# Now restore repository state.
# Ignore failures to get as much cleaned up as possible.
mv -f $TMP/hr/ slhpa/static/slhpa/images/photos/
mv -f $TMP/mr/ slhpa/static/slhpa/images/photos/
mv -f $TMP/lr/ slhpa/static/slhpa/images/photos/
# sed -i 's/DEBUG = False/DEBUG = True/' mysite/settings.py
sed -i 's/ALLOW_EDIT = False/ALLOW_EDIT = True/' mysite/settings.py

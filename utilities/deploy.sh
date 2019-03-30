# Deploy to Google Cloud Platform. Currently *in progress*.
set -x 

if [ "$TMP" = "" ] ; then
    echo No TMP environment variable!
    exit -1
fi

cd ~/Documents/Github/SLHPA-Web-App/mysite                                  ; if [ $? -ne 0 ] ; then exit -6 ; fi
sed -i 's/ALLOW_EDIT = True/ALLOW_EDIT = False/' mysite/settings.py         ; if [ $? -ne 0 ] ; then exit -6 ; fi

# Do this once the base functionality is working.
# sed -i 's/DEBUG = True/DEBUG = False/' mysite/settings.py                 ; if [ $? -ne 0 ] ; then exit -6 ; fi
# TODO : ...and run Django with insecure flag

rm -rf $TMP/photos/                                                         ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f slhpa/static/slhpa/images/photos/ $TMP/                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
mkdir -p slhpa/static/slhpa/images/photos/1/                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
cp $TMP/photos/*.png slhpa/static/slhpa/images/photos/                      ; if [ $? -ne 0 ] ; then exit -6 ; fi
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 ; do
    cp $TMP/photos/1/000000${i}.jpg slhpa/static/slhpa/images/photos/1/     ; if [ $? -ne 0 ] ; then exit -6 ; fi
done

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
rm -rf slhpa/static/slhpa/images/photos/
mv -f $TMP/photos/ slhpa/static/slhpa/images/
sed -i 's/DEBUG = False/DEBUG = True/' mysite/settings.py
sed -i 's/ALLOW_EDIT = False/ALLOW_EDIT = True/' mysite/settings.py

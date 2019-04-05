# Deploy to Google Cloud Platform
echo "Needs more work."
exit 0

set -x 

if [ "$TMP" = "" ] ; then
    echo No TMP environment variable!
    exit -1
fi

cd ~/Documents/Github/SLHPA-Web-App/mysite                                  ; if [ $? -ne 0 ] ; then exit -6 ; fi

rm -rf $TMP/photos/                                                         ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f slhpa/static/slhpa/images/photos/ $TMP/                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
mkdir -p slhpa/static/slhpa/images/photos/1/                                ; if [ $? -ne 0 ] ; then exit -6 ; fi
cp $TMP/photos/*.png slhpa/static/slhpa/images/photos/                      ; if [ $? -ne 0 ] ; then exit -6 ; fi
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 ; do
    cp $TMP/photos/1/000000${i}.jpg slhpa/static/slhpa/images/photos/1/     ; if [ $? -ne 0 ] ; then exit -6 ; fi
done

sed -i 's/ALLOW_EDIT = True/ALLOW_EDIT = False/' mysite/settings.py         ; if [ $? -ne 0 ] ; then exit -6 ; fi

# Do this if we can figure how how to run Django with the insecure flag in GCP.
# sed -i 's/DEBUG = True/DEBUG = False/' mysite/settings.py                 ; if [ $? -ne 0 ] ; then exit -6 ; fi

rm -rf static/                                                              ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py collectstatic                                              ; if [ $? -ne 0 ] ; then exit -6 ; fi

# When running locally, the photos need to be in SLHPA-Web-App/mysite/slhpa/static/slhpa/images/photos/1..3.
# However, in GCP they need to be in SLHPA-Web-App/mysite/static/slhpa/static/slhpa/images//photos/1..3.
# Unclear why this is. To avoid uploading two copies of each photo,
# must temporarily (manually for now) move SLHPA-Web-App/mysite/slhpa/static/slhpa/images/photos/ into a temp location,
# and then back after deployment.

if [ "$WINDIR" = "" ] ; then
    gcloud app deploy                                                       ; if [ $? -ne 0 ] ; then exit -6 ; fi
else
    echo "Now run the following command in a CMD shell:"
    echo "cd Documents\Github\SLHPA-Web-App\mysite\\"
    echo "gcloud app deploy"
    read -p "Press any key to continue after deploy finishes... " -n1 -s
fi

# Now restore repository state.
# Ignore failures to get as much cleaned up as possible.
rm -rf slhpa/static/slhpa/images/photos/
mv -f $TMP/photos/ slhpa/static/slhpa/images/

# sed -i 's/DEBUG = False/DEBUG = True/' mysite/settings.py
sed -i 's/ALLOW_EDIT = False/ALLOW_EDIT = True/' mysite/settings.py

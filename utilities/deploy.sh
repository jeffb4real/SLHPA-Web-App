# Deploy to Google Cloud Platform. Currently *in progress*.
set -x 

if [ "$TMP" = "" ] ; then
    echo No TMP environment variable!
    exit -1
fi

cd ~/Documents/Github/SLHPA-Web-App/mysite                                  ; if [ $? -ne 0 ] ; then exit -6 ; fi
sed -i'.bak' 's/ALLOW_EDIT = True/ALLOW_EDIT = False/' mysite/settings.py   ; if [ $? -ne 0 ] ; then exit -6 ; fi

# Do this once the base functionality is working.
# sed -i'.bak' 's/DEBUG = True/DEBUG = False/' mysite/settings.py             ; if [ $? -ne 0 ] ; then exit -6 ; fi
# TODO : ...and run Django with insecure flag

for t in hr lr mr ; do
    mv slhpa/static/slhpa/images/photos/${t}/ $TMP/                         # ignore failures
done

python manage.py collectstatic                                              ; if [ $? -ne 0 ] ; then exit -6 ; fi
echo "Now run the following command in a CMD shell:"
echo "gcloud app deploy"
read -p "Press any key to continue after deploy finishes... " -n1 -s

# TODO : how to run 'python manage.py migrate' on GCP server?

# Now restore repository state
for t in hr lr mr; do
    mv $TMP/${t} slhpa/static/slhpa/images/photos/                          # ignore failures
done
sed -i'.bak' 's/DEBUG = False/DEBUG = True/' mysite/settings.py             ; if [ $? -ne 0 ] ; then exit -6 ; fi
sed -i'.bak' 's/ALLOW_EDIT = False/ALLOW_EDIT = True/' mysite/settings.py   ; if [ $? -ne 0 ] ; then exit -6 ; fi
rm mysite/settings.py.bak                                                   ; if [ $? -ne 0 ] ; then exit -6 ; fi

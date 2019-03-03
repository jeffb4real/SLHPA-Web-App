# One-time script to handle changing key column to AutoField() in PhotoRecord table.

set -x 

cd ~/Documents/Github/SLHPA-Web-App/mysite                      ; if [ $? -ne 0 ] ; then exit -6 ; fi
if [ -d slhpa/migrations-v1/ ] ; then
    echo "Script has already been run."
    exit -1
fi

git mv slhpa/migrations/ slhpa/migrations-v1/                   ; if [ $? -ne 0 ] ; then exit -6 ; fi
tmpfile=`MKTEMP -p $TMP db.sqlite2.XXX`                         ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv db.sqlite3 $tmpfile                                          ; if [ $? -ne 0 ] ; then exit -6 ; fi

mkdir -p slhpa/migrations/                                      ; if [ $? -ne 0 ] ; then exit -6 ; fi
echo "" > slhpa/migrations/__init__.py                          ; if [ $? -ne 0 ] ; then exit -6 ; fi

# python manage.py migrate --run-syncdb ?

python manage.py makemigrations                                 ; if [ $? -ne 0 ] ; then exit -6 ; fi
python manage.py migrate                                        ; if [ $? -ne 0 ] ; then exit -6 ; fi

# (to create an admin user/pswd to manage admin page)
python manage.py createsuperuser                                ; if [ $? -ne 0 ] ; then exit -6 ; fi

python manage.py runserver                                      ; if [ $? -ne 0 ] ; then exit -6 ; fi
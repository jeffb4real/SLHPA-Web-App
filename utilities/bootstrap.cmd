echo "in progress..."
exit

cd %HOMEDRIVE%%HOMEPATH%\Documents\Github\SLHPA-Web-App\
python -m venv venv
venv\bin\activate.bat
python -m pip install --upgrade pip
pip install -r mysite/requirements.txt
cd mysite\
python manage.py migrate
python manage.py createsuperuser

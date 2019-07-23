rem : CMD script because the gcloud command line utility (sometimes) doesn't echo in git bash.
rem : Currently used only as a source of commands to paste into a CMD window.
rem : python and gloud commands require user input, so this script cannot be run unattended. 
rem : Takes some minutes or hours depending on the number of static files to be collected and uploaded.

pause "Set 'GCP' variables at the end of mysite/mysite/settings.py (unless edit functionality is needed)."

pushd %HOMEDRIVE%%HOMEPATH%\Documents\Github\SLHPA-Web-App\mysite\
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
time < ..\utilities\ret.txt
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
rem : If I get a recommendation to "gcloud components update", I do it. This will take some minutes.
cmd /c "gcloud config list"
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
rem : If not correct project, use this to reset : cmd /c "gcloud config set project slhpa-03"
cmd /c "python manage.py collectstatic"
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
cmd /c "gcloud app deploy"
                                                        rem : don't exit on failure, continue on to clean up
:finish

time < ..\utilities\ret.txt
echo "Browse to .../slhpa/import/transformed to load database (ONLY if necessary)."
pause "Set back 'GCP' variables."
popd

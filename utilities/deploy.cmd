rem : CMD script because the gcloud command line utility (sometimes) doesn't echo in git bash.
rem : python and gloud commands require user input, so this script cannot be run unattended. 
rem : Takes some minutes or hours depending on the number of static files to be collected and uploaded.
rem : It's recommended to first do "gcloud components update". This may take some minutes.

pause "Set ALLOW_EDIT = False in mysite/mysite/settings.py unless import is needed."

pushd %HOMEDRIVE%%HOMEPATH%\Documents\Github\SLHPA-Web-App\mysite\
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
time < ..\utilities\ret.txt
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
cmd /c "python manage.py collectstatic"
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
move /Y slhpa\static\slhpa\images\photos %TMP%
                                                        IF %ERRORLEVEL% NEQ 0 goto :finish
mkdir slhpa\static\slhpa\images\photos\1
                                                        IF %ERRORLEVEL% NEQ 0 goto :restore
mkdir slhpa\static\slhpa\images\photos\2
                                                        IF %ERRORLEVEL% NEQ 0 goto :restore
mkdir slhpa\static\slhpa\images\photos\3
                                                        IF %ERRORLEVEL% NEQ 0 goto :restore
cmd /c "gcloud app deploy"
                                                        rem : don't exit on failure, continue on to clean up
:restore

move /Y %TMP%\photos slhpa\static\slhpa\images

:finish

time < ..\utilities\ret.txt
echo ".../slhpa/import/transformed if necessary."
pause "Set back ALLOW_EDIT = True."
popd

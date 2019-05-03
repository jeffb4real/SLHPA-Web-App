rem : CMD script because the gcloud command line utility (sometimes) doesn't echo in git bash.
rem : python and gloud commands require user input, so this script cannot be run unattended. 
rem : Takes some minutes or hours depending on the number of static files to be collected and uploaded.
rem : It's recommended to first do "gcloud components update". This may take some minutes.

pause "Set ALLOW_EDIT = False in mysite/mysite/settings.py."

pushd %HOMEDRIVE%%HOMEPATH%\Documents\Github\SLHPA-Web-App\mysite\
                                                        IF %ERRORLEVEL% NEQ 0 goto :theend
time < ..\utilities\ret.txt
                                                        IF %ERRORLEVEL% NEQ 0 goto :restore
cmd /c "python manage.py collectstatic"
                                                        IF %ERRORLEVEL% NEQ 0 goto :restore
rmdir /S /Q %TMP%\photos
                                                        rem : don't exit on failure, continue to deploy
move slhpa\static\slhpa\images\photos %TMP%
                                                        IF %ERRORLEVEL% NEQ 0 goto :restore
cmd /c "gcloud app deploy"
                                                        rem : don't exit on failure, continue on to clean up
move %TMP%\photos slhpa\static\slhpa\images

:restore

time < ..\utilities\ret.txt
pause "Set back ALLOW_EDIT = True."
popd

:theend

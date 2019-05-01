rem : CMD script because the gcloud command line utility (sometimes) doesn't echo in git bash.
rem : python and gloud commands require user input, so this script cannot be run unattended. 
rem : Takes a few minutes.

pause "Set ALLOW_EDIT = False in mysite/mysite/settings.py."

pushd %HOMEDRIVE%%HOMEPATH%\Documents\Github\SLHPA-Web-App\mysite\
                                                        IF %ERRORLEVEL% NEQ 0 goto :eof
time < ..\utilities\ret.txt
                                                        IF %ERRORLEVEL% NEQ 0 goto :eof
cmd /c "python manage.py collectstatic"
                                                        IF %ERRORLEVEL% NEQ 0 goto :eof
rmdir /S /Q %TMP%\photos
                                                        IF %ERRORLEVEL% NEQ 0 goto :eof
move slhpa\static\slhpa\images\photos %TMP%
                                                        IF %ERRORLEVEL% NEQ 0 goto :eof
cmd /c "gcloud app deploy"
                                                        IF %ERRORLEVEL% NEQ 0 goto :eof
move %TMP%\photos slhpa\static\slhpa\images

pause "Set back ALLOW_EDIT = True."
time < ..\utilities\ret.txt
popd

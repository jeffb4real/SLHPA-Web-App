echo 'Not tested yet!'
exit -1

set -x
cd ~/Documents/Github/                                          ; if [ $? -ne 0 ] ; then exit -6 ; fi
old=SLHPA-Web-App-${RANDOM}
mv SLHPA-Web-App ${old}                                         ; if [ $? -ne 0 ] ; then exit -6 ; fi
git clone https://github.com/jeffb4real/SLHPA-Web-App.git       ; if [ $? -ne 0 ] ; then exit -6 ; fi
cd SLHPA-Web-App/                                               ; if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f ~/Documents/Github/${old}/mysite/slhpa/static/slhpa/images/ mysite/slhpa/static/slhpa/
                                                                  if [ $? -ne 0 ] ; then exit -6 ; fi
mv -f ~/Documents/Github/${old}/static/ .                       ; if [ $? -ne 0 ] ; then exit -6 ; fi

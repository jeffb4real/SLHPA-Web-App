cd ~/Documents/Github/SLHPA-web-app
python comber.py            ; if [ $? -ne 0 ] ; then exit -6 ; fi
python merger.py            ; if [ $? -ne 0 ] ; then exit -6 ; fi
python transformer.py       ; if [ $? -ne 0 ] ; then exit -6 ; fi
python mapper.py            ; if [ $? -ne 0 ] ; then exit -6 ; fi

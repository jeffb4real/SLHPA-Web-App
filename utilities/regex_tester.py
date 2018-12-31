import re

pattern = r'\D(\d\d\d\d)\D'
pattern = r'^\D*(\d\d\d\d)*\D*$'
pattern = r'^|\D(\d\d\d\d)\D|$'
pattern = r'\D*(\d\d\d\d)\D*'    # works 2nd best for finding year(s)
pattern = r'\b(\d\d\d\d)\b'      # works best for finding year(s)

pattern = r'[\.\?\!][\"\'\)\s]*$'        # find ending punctuation
pattern = r'[\.\?\!\,\'\"][\"\'\)\s]*$'  # find ending punctuation, better

#pattern =   # put your pattern here

while (True):
    print ("\nMatch pattern: %s" % pattern)
    userin = input('Input string: ')
    print ("You entered: ->%s<-" % userin)
    if (re.findall(pattern, userin)):
        print ('match')
    else:
        print ('no match')

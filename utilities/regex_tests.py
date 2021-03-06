import re

patterns = [ r'\D(\d\d\d\d)\D'
            ,r'^\D*(\d\d\d\d)\D*$'
            ,r'^|\D(\d\d\d\d)\D|$'
            ,r'\D*(\d\d\d\d)\D*'    # works 2nd best for finding year(s)
            ,r'\b(\d\d\d\d)\b'      # works best for finding year(s)
            ]

test_strings = ["1872", " 1872", " 1872 ", ".1872", 
                ".1872.", "x1872", "x1872x", "ca1872", "ca.1872","E. 14th and Ward Sts., 1908"]

for pattern in patterns:
    if re.findall(pattern, "18722"):
        print(pattern + " should not find 18722")
    else:
        c = 0
        notfound = ""
        for s in test_strings:
            if (re.findall(pattern, s)):
                c += 1
            else:
                notfound = notfound + " " + s
        if (c == len(test_strings)):
            print(pattern + " : matched " + str(c))
        else:
            print(pattern + " : matched " +  str(c) + ", missed: '" + notfound + "'")

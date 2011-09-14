#!/usr/bin/env python

import crypt
import sys
import random
import string
import getpass

if len(sys.argv) == 2:
    pw1 = getpass.getpass('Enter the password: ')
    pw2 = getpass.getpass('Repeat the password: ')

    if pw1 == pw2:
        salt = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(2))
        print("%s:%s" % (sys.argv[1], crypt.crypt(pw1, salt)))
    else:
        print "Passwords don't match."
else:
    print "Usage: %s username" % sys.argv[0]

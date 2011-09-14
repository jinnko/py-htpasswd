#!/usr/bin/env python

import cgi

import crypt
import sys
import random
import string
import getpass

# DEBUG SUPPORT
#import cgitb
#cgitb.enable()

# HTTP HEADER
print "Content-Type: text/html"
print

# HTTP BODY
print '''<html><head>
    <title>htpasswd.py</title>
    <style type=text/css>
    </style>
    </head>
    <body onload="document.forms.htpasswd.username.focus()">

    <h1>htpasswd.py</h1>
    <p>This script will generate a crypt'd password for use in htpasswd files.</p>
    <p>No support for SHA or MD5 since they're not recognized by nginx.</p>

    <form method=post id=htpasswd>
        <table><tr>
            <th>username:</th>
            <td><input type=text name=username id=username /></td>
        </tr><tr>
            <th>password:</th>
            <td><input type=password name=password /></td>
        </tr><tr>
            <th>repeat:</th>
            <td><input type=password name=password2 /></td>
        </tr><tr>
            <td colspan=2> <input type=submit /> </td>
        </tr></table>
    </form>

    <hr />
'''

form = cgi.FieldStorage()

if "username" in form and "password" in form and "password2" in form:
    username = form['username'].value
    pw1 = form['password'].value
    pw2 = form['password2'].value

    if pw1 == pw2:
        salt = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for x in range(2))
        print "<h2>Generated password</h2>"
        print "<p>Copy and paste this to whoever needs it.</p>"
        print("<p><strong>%s:%s</strong></p>" % (username, crypt.crypt(pw1, salt)))
    else:
        print "<strong>Passwords don't match.</strong>"
else:
    print "<strong>Invalid data provided.</strong>"

print '''
</body>
</html>
'''
#cgi.test()

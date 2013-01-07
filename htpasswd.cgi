#!/usr/bin/env python
#
# @author Jinn Koriech
# @since 2011-09-14
# @url https://github.com/jinnko/py-htpasswd
#
# vim:set ts=4 sw=4 sts=4 expandtab fileencoding=utf8:

import time
start = time.time()
import cgi
import string
import random
import crypt
import hashlib
import bcrypt
import json

# ENABLE FOR DEBUGING
#import cgitb
#cgitb.enable()

# HTTP HEADER
print "Content-Type: text/html"
print

form = cgi.FieldStorage()

if "username" in form and "password" in form and "password2" in form:
    username = form['username'].value
    pw1 = form['password'].value
    pw2 = form['password2'].value

    if pw1 == pw2:
        status = 1
        passes = {}
        # We can't handle bip passwords yet, so just put a place holder there now.
        passes['bip'] = ''

        # Define our random characters that make up our salt
        charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "./"
        charset_hex = "abcdef" + string.digits

        # Crypt
        salt2 = ''.join(random.choice(charset) for x in range(2))
        passes['crypt'] = crypt.crypt(pw1, salt2)

        # CRPYT_MD5
        pw_hash = "MD5"
        salt_len = 16
        salt_prefix = '$1$'
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        passes['crypt_md5'] = {}
        passes['crypt_md5']['pass'] = crypt.crypt(pw1, salt_prefix + salt)
        passes['crypt_md5']['salt'] = salt

        # MD5
        pw_hash = "MD5"
        passes['md5'] = hashlib.md5(pw1).hexdigest()

        # SHA1
        pw_hash = "SHA1"
        salt_len = 32
        salt = ''.join(random.choice(charset_hex) for x in range(salt_len))
        passes['sha1'] = {}
        hashed_password = hashlib.sha1(pw1).hexdigest()
        passes['sha1']['pass'] = hashlib.sha1(salt + hashed_password).hexdigest()
        passes['sha1']['salt'] = salt

        # SHA256
        pw_hash = "SHA256"
        salt_len = 16
        salt_prefix = '$5$rounds=5131$'
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        passes['sha256'] = crypt.crypt(pw1, salt_prefix + salt)

        # SHA512
        pw_hash = "SHA512"
        salt_len = 16
        salt_prefix = '$6$rounds=5131$'
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        passes['sha512'] = crypt.crypt(pw1, salt_prefix + salt)

        # BCrypt
        pw_hash = "bcrypt"
        # use gensalt() default of 12 rounds
        passes['bcrypt'] = bcrypt.hashpw(pw1, bcrypt.gensalt())

    else:
        status = 2
        error = "<strong>Passwords don't match.</strong>"

else:
    status = 0
    error = "<strong>No data provided.</strong>"

##################################################################

# Header
print '''<html><head>
    <title>py-htpasswd</title>
    <style type=text/css>
      body { color: #404040; font-family: courier}
      a { text-decoration: none }
      a:hover { border-bottom: 1px dotted }
    </style>
    </head>
    <body onload="document.forms.htpasswd.username.focus()">

    <table align="center">
        <tr>
            <td valign="top" style="padding-right: 3em;">
    <h1>py-htpasswd</h1>
    <p>Generate crypt'd passwords for use <br />in htpasswd files, haproxy, nginx, etc.</p>
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
            <td colspan=2 style="text-align:right"> <input type=submit value="encrypt" /> </td>
        </tr></table>
    </form>

    <hr />
'''

### BODY
if status == 0:
    print """</td><td>
                <a href="http://xkcd.com/936/"><img src="http://imgs.xkcd.com/comics/password_strength.png" /></a>
            </td>
        </tr><tr>
            <td colspan=2>
    """
elif status == 1:
    print "<h2>Crypted & hashed password</h2>"
    print "<p>Copy and paste this to whoever needs it.</p>"
    print '<pre>"%s": %s</pre>' % (username, json.dumps(passes, indent=2))

else:
    print error

### Footer
print '''   <hr />
            <p><a href="https://github.com/jinnko/py-htpasswd">py-htpasswd</a> executed in {0:.4f} seconds.</p>
        </td>
    </tr>
</table></body></html>
'''.format(time.time() - start)

#cgi.test()

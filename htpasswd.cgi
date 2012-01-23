#!/usr/bin/env python
#
# @author Jinn Koriech
# @since 2011-09-14
# @url https://github.com/jinnko/py-htpasswd
#

import time
start = time.time()

import cgi

import string
import random
import crypt
import hashlib

# ENABLE FOR DEBUGING
#import cgitb
#cgitb.enable()

# HTTP HEADER
print "Content-Type: text/html"
print

# HTTP BODY
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

form = cgi.FieldStorage()

if "username" in form and "password" in form and "password2" in form:
    username = form['username'].value
    pw1 = form['password'].value
    pw2 = form['password2'].value

    if pw1 == pw2:
        charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "./"
        print "<h2>Crypted & hashed password</h2>"
        print "<p>Copy and paste this to whoever needs it.</p>"

        salt2 = ''.join(random.choice(charset) for x in range(2))
        print("<p>Crypt: <strong>%s:%s</strong></p>" % (username, crypt.crypt(pw1, salt2)))

        pw_hash = "MD5"
        salt_len = 16
        salt_prefix = '$1$'
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        print("<p>%s: <strong>%s:%s</strong></p>" % (pw_hash, username, crypt.crypt(pw1, salt_prefix + salt)))

        pw_hash = "SHA1"
        salt_len = 16
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        print("<p>%s: <strong>%s %s salt(%s)</strong></p>" % (pw_hash, username, hashlib.sha1(pw1 + salt).hexdigest(), salt))

        pw_hash = "SHA256"
        salt_len = 16
        salt_prefix = '$5$rounds=5131$'
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        print("<p>%s: <strong>%s:%s</strong></p>" % (pw_hash, username, crypt.crypt(pw1, salt_prefix + salt)))

        pw_hash = "SHA512"
        salt_len = 16
        salt_prefix = '$6$rounds=5131$'
        salt = ''.join(random.choice(charset) for x in range(salt_len))
        print("<p>%s: <strong>%s:%s</strong></p>" % (pw_hash, username, crypt.crypt(pw1, salt_prefix + salt)))

    else:
        print "<strong>Passwords don't match.</strong>"
else:
    print "<strong>No data provided.</strong>"

    print """
            </td>
            <td>
                <a href="http://xkcd.com/936/"><img src="http://imgs.xkcd.com/comics/password_strength.png" /></a>
            </td>
        </tr>
        <tr>
            <td colspan=2>
    """

print '<hr />'
print '<p><a href="https://github.com/jinnko/py-htpasswd">py-htpasswd</a> executed in {0:.4f} seconds.</p>'.format(time.time() - start)

print '''
        </td>
    </tr>
</table>
</body>
</html>
'''
#cgi.test()

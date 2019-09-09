#!/usr/bin/python2.7
print "Content-type:text/html\n"

import sqlite3
import cgi
current_trapdata = []
def create_table():
    conn = sqlite3.connect('trapdata.db')
    c = conn.cursor()
    dbdata_sqlite = """
    CREATE TABLE traps (
    serial text,
    cellnum text,
    email text,
    status text,
    activate text,
    reset text,
    feed text,
    foodcount integer
    )
    """
    c.execute(dbdata_sqlite)
    conn.commit()
    conn.close()

def table_update(item, newval):
    global current_trapdata
    conn = sqlite3.connect('trapdata.db')
    c = conn.cursor()
    c.execute("UPDATE traps SET " + item + " = ? WHERE serial = ?", (newval, current_trapdata[0]))
    conn.commit()
    conn.close()

def add_trap(ser, cel, ema, sta, act, res, fee, foo):
    conn = sqlite3.connect('trapdata.db')
    c = conn.cursor()
    userdata = "INSERT INTO traps (serial, cellnum, email, status, activate, reset, feed, foodcount) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    c.execute(userdata, (ser, cel, ema, sta, act, res, fee, foo))
    conn.commit()
    conn.close()

def find_trap(sn):
    global current_trapdata
    conn = sqlite3.connect('trapdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM traps WHERE serial=?", (sn,))
    current_trapdata = c.fetchone()
    conn.close()

def populate():
    global current_trapdata
    global serial
    print '<!doctype html>'
    print '<html lang="en">'
    print '<head>'
    print '<meta charset="utf-8">'
    print '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    print '<meta name="description" content="Cat Trap">'
    print '<link rel="stylesheet" type="text/css" href="css/trapstyle.css">'
    print '<title>Cat Trap</title>'
    print '</head>'
    print '<body>'
    print '<h1 class="header">Cat Trap</h1>'
    print '<p>Temp for cutting and pasting!: 8165010001</p>'
    print '<div id="displaydiv">'
    print '<p2>Trap & Contact Information</p2>'
    print '<p id="displayp">Trap Serial Number: ' + serial + '</p>'
    print '<p id="trapcell">Contact cell#: (' + current_trapdata[1][0:3] + ') ' + current_trapdata[1][3:6] + '-' + current_trapdata[1][6:10] + '</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print '<input id="cel" type="text" name="cellnum" placeholder="New Cell Number">'
    print '<button id="submitbtn" type="button">Update</button>'
    print '</form>'
    print '<p id="trapemail">Contact E-Mail: ' + current_trapdata[2] + '</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print '<input id="ema" type="email" name="email" placeholder="New E-mail Address">'
    print '<button id="submitbtn" type="button">Update</button>'
    print '</form>'
    print '<h2>Trap Controls</h2>'
    print '<p id="instactivate">If what you see in the trap is the animal you are trying to catch, activate the trap.</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print '<input id="activate" type="number" name="trap" value="1" style="display:none;">'
    print '<button id="submitbtn" type="button">Activate Trap</button>'
    print '</form>'
    print '<p id="foodremaining"> Food servings remaining: ' + str(current_trapdata[7]) + '</p>'
    print '<p id="instfeeder">If the food has been eaten, and you won&#8217;t get there for a while, manually feed the trapped animal.</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print '<input id="feed" type="number" name="dispense" value="1" style="display:none;">'
    print '<button id="submitbtn" type="button">Activate Feeder</button>'
    print '</form>'
    print '<p id="instrefill">If you are refilling the feed magazine:</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print '<input id="addfood" type="number" name="refill" value="1" style="display:none;">'
    print '<button id="submitbtn" type="button">Refill Feeder</button>'
    print '</form>'
    print '<p id="instreset">Release anything caught in the trap, and add more food to the food bowl.</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print '<input id="reset" type="number" name="release" value="1" style="display:none;">'
    print '<button id="submitbtn" type="button">Reset Trap</button>'
    print '</form>'
    print '</div>'
    print '</body>'
    print '</html>'

#create_table()
#add_trap('8165010001', '5707046838', 'zach.ferguson@yahoo.com', 'waiting', 'False', 'False', 'False', 6)

form = cgi.FieldStorage()

serial = form['serial'].value
find_trap(serial)

populate()

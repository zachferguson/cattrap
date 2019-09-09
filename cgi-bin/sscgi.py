# {'8165010001': {'trapserial': '8165010001', 'cell': 5707046838, 'email': 'zach.ferguson@yahoo.com', 'activate': false, 'reset': false, 'foodcount': 6, 'image': '/trapper/8165010001.jpg'}
# serial, cell, email, activate, reset, foodcount, image,

import sqlite3

current_trapdata = []
#later:  form = cgi.FieldStorage()
'''
    later!!!
    if form.getValue('serial'):
        serial = form.getValue('serial')
'''

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
    print('table named traps created')

def add_trap(ser, cel, ema, sta, act, res, fee, foo):
    conn = sqlite3.connect('trapdata.db')
    c = conn.cursor()
    print('database created / accessed')
    userdata = "INSERT INTO traps (serial, cellnum, email, status, activate, reset, feed, foodcount) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
    print('executing add record')
    c.execute(userdata, (ser, cel, ema, sta, act, res, fee, foo))
    print('added record')
    conn.commit()
    conn.close()

def find_trap(sn):
    global current_trapdata
    conn = sqlite3.connect('trapdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE serial=?", (sn,))
    current_trapdata = c.fetchone()
    print(current_trapdata)
    conn.close()

def populate():
    '''
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
    print '<h2 class="header">Cat Trap</h2>'
    print '<p>Thank you for helping capture and spay/neuter stray and feral cats!</p>'
    print '<p>Please enter the serial number of your trap to access it&#8217;s functions.</p>'
    print '<p>Temp for cutting and pasting!: 8165010001</p>'
    print '<form method="POST" action="/cgi-bin/ctcgi.py">'
    print 'Serial Number: <input id="ser" type="number" name="serial">'
    print '<button id="submitbtn" type="button">Submit</button>'
    print '</form>'
    print '<div id="displaydiv">'
    print '<p id="displayp"></p>'
    print '<p id="trapcell">' + current_trapdata[1] + '</p>'
    #<button id="changecell" class="ctrlbtn" type="button">Change Cell Number</button>
	print '<p id="trapemail">' + current_trapdata[2] + '</p>'
	#<button id="changeemail" class="ctrlbtn" type="button">Change Email</button>
	print '<p id="foodremaining">' + str(current_trapdata[7]) + '</p>'
	print '<p id="instactivate">If what you see in the trap is the animal you are trying to catch, activate the trap.</p>'
	#<button id="btnactivate" class="ctrlbtn" type="button">Activate Trap</button>
	print '<p id="instreset">Release anything caught in the trap, and add more food to the food bowl.</p>'
	#<button id="btnreset" class="ctrlbtn" type="button">Reset Trap</button>
	print '<p id="instfeeder">If the food has been eaten, and you won&#8217;t get there for a while, manually feed the trapped animal.</p>'
	#<button id="btnfeeder" class="ctrlbtn" type="button">Activate Feeder</button>
    print '</div>'
    print '</body>'
    print '</html>'
    '''
create_table()
add_trap('8165010001', '5707046838', 'zach.ferguson@yahoo.com', 'waiting', 'False', 'False', 'False', 6)
#find_trap('8165010001')
#print(current_trapdata)

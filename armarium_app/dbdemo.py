### optional DB query script ###

### RUN USING PYTHON 3 ###
### Must be in same directory as app.db ###
### Asks user to input a manuscript ID number, returns small
### subset of data (manuscript info and volume info for that manuscript)
### in response to query ***

import sqlite3


conn = sqlite3.connect('app.db')

#c = conn.cursor()
conn.row_factory = sqlite3.Row
c = conn.cursor()

msshelfmark = ''
while type(msshelfmark ) != int:
	msshelfmark = input('Enter a shelfmark number (valid integer) from 1 to 308: ')
	try:
		msshelfmark = int(msshelfmark)
	except:
		continue

c.execute('SELECT * FROM manuscript WHERE id=?', [msshelfmark])
ms = c.fetchone()
if ms == None:
	print('No record with that number in database.')
	exit()
cols = ms.keys()

print('Manuscript info: ')
for x in range(0,len(ms)):
	print(cols[x], ': ', ms[x])



c.execute('SELECT * FROM volume WHERE ms_id=?', [msshelfmark])
vols = c.fetchall()
print('\nVolume info: ')
for codex in vols:
	volcols = codex.keys()
	for columns in range(0, len(volcols)):
		print(volcols[columns], codex[columns])
	print('\n')

#c.execute('SELECT * FROM manuscript WHERE id=?', [msshelfmark])

#print

conn.close()
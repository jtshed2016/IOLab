from flask import render_template, redirect, request
from app import app, models, db
#need to create "forms.py" doc in "app" directory when I determine needs
#from .forms import CustomerForm, AddressForm, OrderForm
from .data_parse_and_load import load
import json, re, csv
#from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
#load data
sourcefile = 'trial_II160119.json'
sourceobj = open(sourcefile)
sourcedict = json.load(sourceobj)
sourceobj.close()

#parse data
allrecs = load(sourcedict)

#load mss into database
for record in allrecs:
	if record == 'RobbinsMSCould not find valid shelfmark':
		continue
	print(record)
	#print(allrecs[record])
	#print(int(allrecs[record]['shelfmark'].split(' ')[2]))
	print('\n')



	ms = models.manuscript(
		id = int(allrecs[record]['shelfmark'].split(' ')[2]),
		shelfmark = allrecs[record]['shelfmark'],
		date1 = allrecs[record]['date1'],
		date2 = allrecs[record]['date2'],
		datetype = allrecs[record]['datetype'],
		language = allrecs[record]['language'],
		num_volumes = allrecs[record]['volumes']
		)
	db.session.add(ms)

	db.session.commit()

	for msvol in allrecs[record]['volumeInfo']:
		#print(msvol)
		volItem = models.volume(
			support = allrecs[record]['support'],
			extent = msvol['extent'],
			extent_unit = msvol['extentUnit'],
			bound_width = msvol['boundWidth'],
			bound_height = msvol['boundHeight'],
			leaf_width = msvol['supportWidth'],
			leaf_height = msvol['supportHeight'],
			written_width = msvol['writtenWidth'],
			written_height = msvol['writtenHeight'],
			size_unit = msvol['units'],
			quire_register = msvol['quires'],
			phys_arrangement = msvol['arrangement'],
			ms_id = ms.id
			)
		db.session.add(volItem)
		
		if 'watermarks' not in msvol:
			print allrecs[record]

		for ms_wm in msvol['watermarks']:
			wmQuery = models.watermark.query.get(ms_wm[0])
			if wmQuery == None:
				wmItem  = models.watermark(
					id = ms_wm[0],
					name = ms_wm[1],
					url = ms_wm[2],
					mss = [models.manuscript.query.get(ms.id)]
					)
				db.session.add(wmItem)
			else:
				wmItem = models.watermark.query.get(ms_wm[0])
				wmItem.mss.append(models.manuscript.query.get(ms.id))


	db.session.commit()

	for title in allrecs[record]['titles']:
		titleInstance = models.title(
			title_text = title['text'],
			title_type = title['type'],
			ms_id = ms.id
			)
		db.session.add(titleInstance)
	db.session.commit()

	for person in allrecs[record]['people']:
		print(person)
		print(allrecs[record]['people'][person])
		print(allrecs[record]['people'][person]['relationship'])

		personQuery = models.person.query.filter_by(name_simple=person).first()
		if personQuery == None:
			personRec = models.person(
				name_simple = person,
				name_display = allrecs[record]['people'][person]['displayName'],
				name_fuller = allrecs[record]['people'][person]['Fullname'],
				year_1 = allrecs[record]['people'][person]['date1'],
				year_2 = allrecs[record]['people'][person]['date2'],
				datetype = allrecs[record]['people'][person]['datetype'],
				numeration = allrecs[record]['people'][person]['Numeration'],
				title = allrecs[record]['people'][person]['Title']
				)
			db.session.add(personRec)
			db.session.commit()
			
			#new query of newly committed person entity to get ID
			newPersonRecord = models.person.query.filter_by(name_simple=person).first()
			for rel in allrecs[record]['people'][person]['relationship']:
				relRec = models.person_ms_assoc(
					person_id = newPersonRecord.id,
					ms_id = ms.id,
					assoc_type = rel
					)
				db.session.add(relRec)
				db.session.commit()

		else:
			for rel in allrecs[record]['people'][person]['relationship']:
				relRec = models.person_ms_assoc(
					person_id = personQuery.id,
					ms_id = ms.id,
					assoc_type = rel
					)
				db.session.add(relRec)
				db.session.commit()
"""

@app.route('/')
def homepage():

	return render_template('home.html')

@app.route('/add_ms', methods = ['GET', 'POST'])
def add_ms():
	pass

@app.route('/list_mss', methods = ['GET'])
def list_mss():
	allmss = models.manuscript.query.all()
	return render_template('home2.html', recs = allmss)

@app.route('/ms<idno>', methods = ['GET'])
def ms_view(idno):
	"""Page view for individual MS"""
	
	focusms = models.manuscript.query.get(idno)
	print(focusms.shelfmark)

@app.route('/search', methods = ['GET', 'POST'])
def mss_search():
	pass

#@app.route('/<facet>/<value>', methods = ['GET'])
#def show_facet():
	#Linking from a list or individual MS page
	#show all MSS that share this attribute

	#Need to redo this: set up as a GET and get arguments to use as DB queries 

#	pass
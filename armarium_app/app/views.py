import os, sys

relpath = os.path.dirname(__file__)
sys.path.append(relpath)

from flask import render_template, redirect, request
from flask.json import dumps, jsonify
from app import app, models, db
from .forms import SearchForm
from .data_parse_and_load import load
import json, re, csv
#from urllib.request import urlopen
from bs4 import BeautifulSoup
from sqlalchemy import func, distinct


'''
print(relpath)

#load data
sourcefile = os.path.join(relpath, 'trial_II160119.json')
sourceobj = open(sourcefile)
sourcedict = json.load(sourceobj)
sourceobj.close()

#parse data
allrecs = load(sourcedict)

#load mss into database
for record in allrecs:
	if record == 'RobbinsMSCould not find valid shelfmark':
		continue
	print record
	#print(allrecs[record]['places'])
	#for place in allrecs[record]['places']:
	#	print '\t', place, 'type:', allrecs[record]['places'][place]
	#print allrecs[record]['publisher']
	#print '\n'


	#print(record)
	#print(allrecs[record])
	#print(int(allrecs[record]['shelfmark'].split(' ')[2]))
	#print('\n')





	ms = models.manuscript(
		id = int(allrecs[record]['shelfmark'].split(' ')[2]),
		shelfmark = allrecs[record]['shelfmark'],
		date1 = allrecs[record]['date1'],
		date2 = allrecs[record]['date2'],
		datetype = allrecs[record]['datetype'],
		language = allrecs[record]['language'],
		num_volumes = allrecs[record]['volumes'],
		summary = allrecs[record]['summary'],
		ownership_history = allrecs[record]['ownership_history']

		)
	db.session.add(ms)

	db.session.commit()

	#iterate over volumes to add volume-specific entities (volume attributes, watermarks, content items)
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
		db.session.commit()
		#commit here to have id
		
		#if 'watermarks' not in msvol:
			#print allrecs[record]

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

		for contentItem in msvol['contents']:
			contentObj = models.content_item(
				text = contentItem['text'],
				fol_start_num = contentItem['startFol'],
				fol_start_side = contentItem['startSide'],
				fol_end_num = contentItem['endFol'],
				fol_end_side = contentItem['endSide'],
				ms_id = ms.id,
				vol_id = volItem.id
				)
			db.session.add(contentObj)


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
		#print(person)
		#print(allrecs[record]['people'][person])
		#print(allrecs[record]['people'][person]['relationship'])

		#check to see if person is already in database; 
		#if not, add to DB
		#if so, retrieve and add new relationships
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

	for placelisting in allrecs[record]['places']:
		#iterate over places
		#check db to see if it exists
		placeQuery = models.place.query.filter_by(place_name = placelisting['name']).first()
		if placeQuery == None:
		#if not, create new place
			addedPlace = models.place(
				place_name = placelisting['name'],
				place_type = placelisting['type'],
				lat = placelisting['lat'],
				lon = placelisting['lon'],
				mss = [models.manuscript.query.get(ms.id)]
				)
			db.session.add(addedPlace)
			db.session.commit()
		else:
			placeQuery.mss.append(models.manuscript.query.get(ms.id))
			db.session.commit()

'''

@app.route('/')
def homepage():
	lats = 0
	lons = 0
	count = 0
	placedict = {}

	allmss = models.manuscript.query.all()
	for ms in allmss:
		count +=1
		for allPlace in ms.places:
			if allPlace.place_type == 'country':
				
				if allPlace.place_name not in placedict:
					placedict[allPlace.place_name] = {'center': {'lat': allPlace.lat, 'lng': allPlace.lon}, 'count': 1}
				else:
					placedict[allPlace.place_name]['count'] += 1
					lats = lats + allPlace.lat
					lons = lons + allPlace.lon

	avlats = lats/count
	avlons = lons/count
	#print placedict
	print avlats, avlons
	placeobj = dumps(placedict)
	#need to use regex to remove quotes in json string and 
	subbedplace =re.sub(r'[\"\' ]', '', placeobj)
	print(subbedplace)

	return render_template('home.html', avgLat = avlats, avgLon = avlons, places=subbedplace, pagetitle = 'Manuscripts of the Robbins Collection')

@app.route('/add_ms', methods = ['GET', 'POST'])
def add_ms():
	#to be implemented later
	pass

@app.route('/list_mss', methods = ['GET'])
def list_mss():
	allmss = models.manuscript.query.all()
	return render_template('home2.html', recs = allmss)

@app.route('/ms<idno>', methods = ['GET'])
def ms_view(idno):
	"""Page view for individual MS"""
	
	pagems = models.manuscript.query.get(idno)

	#pagedict: dictionary of nodes and links in a graph centered on the MS; to be used for vis
	pagedict = {'nodes': [{"name": pagems.shelfmark, "group": 0, "role": 'manuscript', "dbkey": pagems.id}], 'links': []}
	index = 1
	for person_rel in pagems.assoc_people:
		pagedict['nodes'].append({"name": person_rel.person.name_display, "group": 1,
		 "role": person_rel.assoc_type, "dbkey": person_rel.person.id})
		pagedict['links'].append({"source": index, "target": 0, "value": 10})
		index +=1

	for place_rel in pagems.places:
		pagedict['nodes'].append({"name": place_rel.place_name, "group": 2, "role": place_rel.place_type, "dbkey": place_rel.id})
		pagedict['links'].append({"source": index, "target": 0, "value": 10})
		index +=1

	#if pagems.publisher
	#publisher not yet implemented, but need to add
	#print(pagedict)

	graphobj = json.dumps(pagedict)
	#graphobj = jsonify(pagedict)
	
	return render_template('msview.html', pagetitle = pagems.shelfmark, ms=pagems, graphsend=graphobj)

@app.route('/search', methods = ['GET', 'POST'])
def mss_search():
	#needs lots of work, not yet fully implemented
	searchform = SearchForm()
	if searchform.validate_on_submit():
		searchquery = searchform.searchfield.data
		results = models.manuscript.query.filter(searchquery in manuscript.summary)
		print(results)
		return render_template('searchresult.html', results =results)

@app.route('/places', methods = ['GET'])
def list_places():
	place_list = models.place.query.all()

	return render_template('placelist.html', recs=place_list, pagetitle='Places of the Robbins Manuscripts')


@app.route('/place<placeid>', methods = ['GET'])
def view_place(placeid):
	#show info about a place in conjunction with their relationships with MSS
	focusplace = models.place.query.get(placeid)
	return render_template ('placeview.html', location=focusplace, pagetitle=focusplace.place_name + ' in the Robbins Manuscripts')

@app.route('/person<personid>', methods = ['GET'])
def view_person(personid):
	#show info about a person in conjunction with their relationships with MSS
	focusperson = models.person.query.get(personid)

	return render_template('personview.html', person = focusperson, pagetitle = focusperson.name_display + ' in the Robbins Manuscripts')

@app.route('/people', methods = ['GET'])
def list_people():
	allpeople = models.person.query.order_by(models.person.name_display).all()

	return render_template('personlist.html', pagetitle='People in the Robbins Manuscripts', people=allpeople)

@app.route('/watermark<wmid>', methods = ['GET', 'POST'])
def view_wm(wmid):
	#show info about a watermark, link to Briquet page, graph of use in MSS
	page_wm = models.watermark.query.get(wmid)
	
	return render_template('wmview.html', mainwm = page_wm, pagetitle = page_wm.name + ', ' + str(page_wm.id))

@app.route('/watermarks', methods = ['GET'])
def list_watermarks():
	returnlist = []
	wmtypes = models.watermark.query.group_by(models.watermark.name).all()
	for x in wmtypes:
		holder = []
		for y in models.watermark.query.filter_by(name=x.name).all():
			holder.append(y)
		returnlist.append((x, holder))
	return render_template('wmlist.html', pagetitle='Watermarks', recs = returnlist)



@app.route('/sendjson', methods = ['GET'])
def send_json():
	#return JSON of relationships, to expand and re-render graphs
	valuemap = {'manuscript': models.manuscript, 'person': models.person, 'watermark': models.watermark, 'place': models.place}
	table = request.args.get('entity')
	ent_id = request.args.get('id')
	result = valuemap[table].query.get(ent_id)

	returndict = {'nodes': [], 'links': []}
	index = 1
	#index starts from 0; on transferring to vis, will have to append and adjust indices
	if table == 'manuscript':
		#this function was called from a manuscript; send back MS and related entities
		#don't need the manuscript itself; calling item is already in the graph and doesn't need to be added
		#actually, this is contextually dependent; need to figure out a way to deal
		for person_rel in result.assoc_people:
			returndict['nodes'].append({'name': person_rel.person.name_display, 'group': 1,
			 'role': person_rel.assoc_type, "dbkey": person_rel.person.id})
			returndict['links'].append({'source': index, 'target': 0, 'value': 10})
			index +=1

		for place_rel in result.places:
			returndict['nodes'].append({"name": place_rel.place_name, "group": 2, "role": place_rel.place_type, "dbkey": place_rel.id})
			returndict['links'].append({"source": index, "target": 0, "value": 10})
			print place_rel.place_name, place_rel.lat, place_rel.lon
			index +=1

		for wm in result.watermarks:
			returndict['nodes'].append({'name': wm.name, 'group': 3, 'role': 'watermark', 'dbkey': wm.id})
			returndict['links'].append({'source': index, 'target': 0, 'value': 10})
			index +=1
		#need to add orgs, external docs, subject, publisher here when implemented

		return jsonify(returndict)

	elif table == 'person':
		returndict['nodes'].append({'name': result.name_display, 'group': 1, 'role': '', 'dbkey': result.id})
		#returndict['links'].append({'source': index, 'target': 0, 'value': 10})
		index +=1

		for ms_rel in result.ms_relations:
			returndict['nodes'].append({'name': models.manuscript.query.get(ms_rel.ms_id).shelfmark, 'group': 0, 'role': 'manuscript', 'dbkey': ms_rel.id})
			returndict['links'].append({'source': index, 'target': 0, 'value': 10})
			index +=1

		return jsonify(returndict)

	elif table == 'watermark':
		returndict['nodes'].append({'name': ('Watermark '+ result.name), 'group': 3, 'role': 'watermark', 'dbkey': result.id})
		
		for ms_rel in result.mss:
			returndict['nodes'].append({'name': ms_rel.shelfmark, 'group': 0, 'role': 'manuscript', 'dbkey': ms_rel.id})
			returndict['links'].append({'source': index, 'target': 0, 'value': 10})
			index +=1

		return jsonify(returndict)

	elif table == 'place':
		returndict['nodes'].append({'name': (result.place_name), 'group': 1, 'role': 'place', 'dbkey': result.id})
		
		for ms_rel in result.mss:
			returndict['nodes'].append({'name': ms_rel.shelfmark, 'group': 0, 'role': 'manuscript', 'dbkey': ms_rel.id})
			returndict['links'].append({'source': index, 'target': 0, 'value': 10})
			index +=1

		return jsonify(returndict)

	else:
		raise NotImplentedError('Entity not yet implemented')


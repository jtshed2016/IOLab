from app import db

#association table for a manuscript and a watermark (see below)
has_watermark = db.Table('has_watermark',
	db.Column('ms_id', db.Integer, db.ForeignKey('manuscript.id')),
	db.Column('wm_id', db.Integer, db.ForeignKey('watermark.id'))
	)

#association table for manuscript and place
has_place = db.Table('has_place',
	db.Column('ms_id', db.Integer, db.ForeignKey('manuscript.id')),
	db.Column('place_id', db.Integer, db.ForeignKey('place.id'))
	)


#the central entity of the system, representing a unified textual item
class manuscript(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	shelfmark = db.Column(db.String(15))
	date1 = db.Column(db.Integer)
	date2 = db.Column(db.Integer)
	datetype = db.Column(db.Integer)
	language = db.Column(db.String(60))
	summary = db.Column(db.String(1000))
	#520
	ownership_history = db.Column(db.String(1000))
	#561
	num_volumes = db.Column(db.Integer)
	#relationships
	volumes = db.relationship('volume',
		backref = 'ms',
		lazy='dynamic')
	contents = db.relationship('content_item', 
		backref = 'ms', 
		lazy='dynamic')
	titles = db.relationship('title', 
		backref = 'ms', 
		lazy='dynamic'
		)
	watermarks = db.relationship('watermark',
		secondary = has_watermark,
		backref = db.backref('mss', lazy='dynamic')
		)
	assoc_people = db.relationship('person_ms_assoc',
		backref = 'ms',
		lazy='dynamic')
	places = db.relationship('place',
		secondary = has_place,
		backref = db.backref('mss', lazy='dynamic')
		)


	def __repr__(self):
		return self.shelfmark

#the physical manifestation of a manuscript; there may be more than one
#for a multi-volume item
class volume(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	ms_format = db.Column(db.String(20))
	support = db.Column(db.String(15))
	extent = db.Column(db.Integer)
	extent_unit = db.Column(db.String(3))
	bound_width = db.Column(db.Integer)
	bound_height = db.Column(db.Integer)
	leaf_width = db.Column(db.Integer)
	leaf_height = db.Column(db.Integer)
	written_width = db.Column(db.Integer)
	written_height = db.Column(db.Integer)
	size_unit = db.Column(db.String(3))
	written_lines = db.Column(db.Integer)
	quire_register = db.Column(db.String(60))
	phys_arrangement = db.Column(db.String(60))
	decoration = db.Column(db.String(1000))
	contents = db.relationship('content_item', 
		backref = 'volume', 
		lazy='dynamic')

	ms_id = db.Column(db.Integer, db.ForeignKey('manuscript.id'))
	

#a discrete textual item in a manuscript
class content_item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(1000))
	fol_start_num = db.Column(db.Integer)
	fol_start_side = db.Column(db.String(1))
	fol_end_num = db.Column(db.Integer)
	fol_end_side = db.Column(db.String(1))

	ms_id = db.Column(db.Integer, db.ForeignKey('manuscript.id'))
	vol_id = db.Column(db.Integer, db.ForeignKey('volume.id'))

#a person related to a manuscript or text
class person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name_display = db.Column(db.String(200))
	name_simple = db.Column(db.String(200))
	name_fuller = db.Column(db.String(200))
	year_1 = db.Column(db.Integer)
	year_2 = db.Column(db.Integer)
	datetype = db.Column(db.Integer)
	numeration = db.Column(db.String(20))
	title = db.Column(db.String(30))
	ms_relations = db.relationship('person_ms_assoc', 
		backref = 'person', 
		lazy='dynamic')

#an association between a person and a manuscript;
#rendered as a full model to capture nature of relationship
class person_ms_assoc(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
	ms_id = db.Column(db.Integer, db.ForeignKey('manuscript.id'))
	assoc_type = db.Column(db.String(50))

#support, format, datetype as separate lookup table?

#title of a manuscript, whether main or alternate name/spelling
class title(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title_text = db.Column(db.String(150))
	title_type = db.Column(db.String(20))
	#possible values are main, uniform, varying, secundo folio
	ms_id = db.Column(db.Integer, db.ForeignKey('manuscript.id'))

	def __repr__(self):
		return self.title_text

#a watermark in the manuscript's support
class watermark(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40))
	url = db.Column(db.String(100))

	def __repr__(self):
		return '<watermark Briquet ' + self.name + str(self.id) + '>'

class place(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	place_name = db.Column(db.String(60))
	place_type = db.Column(db.String(10))
	lat = db.Column(db.Float)
	lon = db.Column(db.Float)

	def __repr__(self):
		return '<place ' + self.place_name + ' (' + self.place_type + ')>'


'''
Python file containing all model components for web application Fyyur, i.e.,
- model definition for Show, Venue and Artist
- connecting to db
- migrations
'''
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Initialized without explicit app (Flask instance)
db = SQLAlchemy()

# TODO: Implement Show and Artist models, and complete all model relationships 
# and properties, as a database migration.

# create an association table for the many-to-many-relationship between venues 
# and artists
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        '''
        Representation function for shows
        '''
        return 'Show Id:{} - Start Time {}'.format(self.id, self.start_time)


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String) # name of venue
    city = db.Column(db.String(120)) # city of venue
    state = db.Column(db.String(120)) # state, where city is located
    address = db.Column(db.String(120)) # full address of venue
    phone = db.Column(db.String(120)) # phone contact of venue
    image_link = db.Column(db.String(500)) # link to image of venue
    facebook_link = db.Column(db.String(120)) # link to facebook page of venue
    website_link = db.Column(db.String(120)) # link to website of venue
    # TODO: implement any missing fields, as a database migration using 
    # # Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120))) # genres of the venue
    # # information if venue is seeking artists or not
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False) 
    seeking_description = db.Column(db.String(500)) # optional seeking description
    # many-to-many relationship to Artists via 'Show'
    shows = db.relationship('Show', backref='venue', lazy='joined', cascade="all, delete")

    def __repr__(self):
        '''
        Representation function for venues
        '''
        return 'Venue Id:{} - Name: {}'.format(self.id, self.name)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String) # name of artist
    city = db.Column(db.String(120)) # name of city, the artist is located
    state = db.Column(db.String(120)) # state of where city is located
    phone = db.Column(db.String(120)) # phone contact of artist
    genres = db.Column(db.ARRAY(db.String())) # genres of the artist
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using 
    # Flask-Migrate
    # information if artist is seeking venues or not
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False) 
    seeking_description = db.Column(db.String(500)) # optional seeking description
    website_link = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist', lazy='joined', cascade="all, delete")

    def __repr__(self):
        '''
        Representation function for artists
        '''
        return 'Artist Id:{} - Name: {}'.format(self.id, self.name)
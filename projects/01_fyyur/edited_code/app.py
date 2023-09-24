'''
Python file containing all central components for configuring and running the web application Fyyur, i.e.,
- import and/or definition of all required functions
- definition of app
- connecting to db
- application logic and app controller
- views
'''
#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
import sys
from forms import *
from config import SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# define and configure the app and connect a database object
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# TODO: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# create an association table for the many-to-many-relationship between venues and artists
Show = db.Table('Show', db.Model.metadata,
    db.Column('Venue_id', db.Integer, db.ForeignKey('Venue.id')),
    db.Column('Artist_id', db.Integer, db.ForeignKey('Artist.id')),
    db.Column('start_time', db.DateTime)
)

class Venue(db.Model):
  __tablename__ = 'Venue'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String) # name of venue
  city = db.Column(db.String(120)) # city of venue
  state = db.Column(db.String(120)) # state, where city is located
  address = db.Column(db.String(120)) # full address of venue
  phone = db.Column(db.String(120)) # phone contact of venue
  image_link = db.Column(db.String(500)) # link to image of venue
  facebook_link = db.Column(db.String(120)) # link to facebook page of venue
  website_link = db.Column(db.String(120)) # link to website of venue
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  genres = db.Column(db.ARRAY(db.String(120))) # genres of the venue (use of array, because multiple genres in one venue are possible)
  seeking_talent = db.Column(db.Boolean, nullable=False, default=False) # information if venue is seeking artists or not
  seeking_description = db.Column(db.String(500)) # optional seeking description
  venues = db.relationship('Artist', secondary=Show, backref=db.backref('shows', lazy='joined')) # many-to-many relationship to Artists via association table 'Show'

  def __repr__(self):
      '''
      Representation function for venues
      '''
      return 'Venue Id:{} - Name: {}'.format(self.id, self.name)

class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String) # name of artist
  city = db.Column(db.String(120)) # name of city, the artist is located
  state = db.Column(db.String(120)) # state of where city is located
  phone = db.Column(db.String(120)) # phone contact of artist
  genres = db.Column(db.ARRAY(db.String())) # genres of the artist (use of array, because artists could play multiple genres)
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  seeking_venue = db.Column(db.Boolean, nullable=False, default=False) # information if artist is seeking venues or not
  seeking_description = db.Column(db.String(500)) # optional seeking description
  website_link = db.Column(db.String(120))

  def __repr__(self):
      '''
      Representation function for artists
      '''
      return 'Artist Id:{} - Name: {}'.format(self.id, self.name)

with app.app_context():
  db.create_all()

#----------------------------------------------------------------------------#
# Custom Functions.
#----------------------------------------------------------------------------#

def object_as_dict(obj):
  '''
  Converts SQLALchemy query results to dictionary

  Source: https://riptutorial.com/sqlalchemy/example/6614/converting-a-query-result-to-dict
  '''
  return {c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs}

def get_dict_list_from_result(result):
  '''
  Converts SQLALchemy collections results (sqlalchemy.util._collections.result) to dictionary

  Source: https://stackoverflow.com/questions/48232222/how-to-deal-with-sqlalchemy-util-collections-result
  '''
  list_dict = []
  for i in result:
      i_dict = i._asdict()  
      list_dict.append(i_dict)
  return list_dict

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  '''
  Converts datetime to user's local datetime
  '''
  date = dateutil.parser.parse(str(value))
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  '''
  Controller for homepage (template/pages/home.html) of Fyyur with following functions
  - create new artists
  - create new venues
  - create new shows
  - search function for artists and venues
  - show list of recently created artists and venues
  '''
  # query database for recently created artists and venues
  recent_artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  recent_venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
  # list recently created artists and venues
  return render_template('pages/home.html', recent_artists = recent_artists, recent_venues = recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  '''
  Controller for venue page (template/pages/venues.html) of Fyyur with following functions
  - show list of all venues
  - group list by location (city, state)
  - show number 
  '''
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  # create a list of dictionaries of the cities and states of venues
  data = get_dict_list_from_result(db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state))

  # determine number of shows in same city and venue by creating a new key in the dictionary, that contains a list of venues that are located in the same city
  for location in data:
    location['venues'] = [object_as_dict(venue) for venue in Venue.query.filter_by(city = location['city']).all()]
    for venue in location['venues']:
      # determine number of upcoming shows
      venue['num_shows'] = db.session.query(func.count(Show.c.Venue_id)).filter(Show.c.Venue_id == venue['id']).filter(Show.c.start_time > datetime.now()).all()[0][0]
  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
  '''
  Controller for venues' search page (template/pages/search_venues.html) of Fyyur with following functions
  - search for venues (get list of results that match the search term)
  - return number of database entries that match the search term
  - redirect to venue page
  '''
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  # get search term from request
  search_term = request.form.get('search_term', '')

  # query database entries of venues that contain the search term
  data = Venue.query.filter(Venue.name.contains(search_term)).all()

  # count query results
  data_count = db.session.query(func.count(Venue.id)).filter(Venue.name.contains(search_term)).all()
  
  # create a dictionary with the results of the search
  response={
    "count": data_count,
    "data": data
    }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  '''
  Controller for the venue page (template/pages/venues/<int:venue_id>.html) of Fyyur with following functions
  - show all information of venue database entries
  - show list of shows (past and upcoming)
  - delete venue
  '''
  # TODO: replace with real venue data from the venues table, using venue_id

  # get database entry by id
  venue = Venue.query.get(venue_id)

  # get shows of venue (past and upcoming)
  # get the artist's name and image to show on page
  # count shows
  venue.past_shows = (db.session.query(
    Artist.id.label("artist_id"), 
    Artist.name.label("artist_name"), 
    Artist.image_link.label("artist_image_link"), 
    Show)
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.Artist_id == Artist.id)
    .filter(Show.c.start_time <= datetime.now())
    .all())
  
  venue.past_shows_count = (db.session.query(
    func.count(Show.c.Venue_id))
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.start_time <= datetime.now())
    .all())[0][0]

  venue.upcoming_shows = (db.session.query(
    Artist.id.label("artist_id"), 
    Artist.name.label("artist_name"), 
    Artist.image_link.label("artist_image_link"), 
    Show)
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.Artist_id == Artist.id)
    .filter(Show.c.start_time > datetime.now())
    .all())
  
  venue.upcoming_shows_count = (db.session.query(
    func.count(Show.c.Venue_id))
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.start_time > datetime.now())
    .all())[0][0]
  
  print(venue.past_shows)

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  '''
  Controller for the create venue page (template/pages/venues/create.html) of Fyyur with following functions
  - show blank create venue form
  '''
  # initialize VenueForm
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  '''
  Controller for the create venue page (template/pages/venues/create.html) of Fyyur with following functions
  - handle submitted venue data
  - create new venue
  - error handling
  '''

  # TODO: insert form data as a new Venue record in the db, instead
  # create form for request venue data
  form = VenueForm(request.form)

  # TODO: modify data to be the data object returned from db insertion
  # validate form input
  if form.validate():
    try:
      # create new venue instance with form data
      newVenue = Venue(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        address = request.form['address'],
        phone = request.form['phone'],
        image_link = request.form['image_link'],
        # seeking_talent = request.form['seeking_talent'],
        seeking_description = request.form['seeking_description'],
        website_link = request.form['website_link'],
        genres = request.form.getlist('genres'),
        facebook_link = request.form['facebook_link'])

      # add and commit transaction
      with app.app_context():
        db.session.add(newVenue)
        db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # rollback session in case of error
      db.session.rollback()
      # print error
      print(sys.exc_info())
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
      # close session
      db.session.close()
  else:
    # flash validation error
    flash(form.errors)
    flash('An error occurred due to form validation. Venue {} could not be listed.'.format(request.form['name']))

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  '''
  Controller for the delete venue page (template/pages/venues/<venue_id>.html) of Fyyur with following functions
  - delete existing venue database entry
  - error handling
  '''
  
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  try:
    # delete database entry selected by venue_id
    Venue.query.filter_by(id=venue_id).delete()
    # commit transaction
    db.session.commit()
  except:
    # rollback session in case of error
    db.session.rollback()
    # print error
    print(sys.exc_info())
    # return error
    return jsonify({'success': False})
  finally:
    # close session
    db.session.close()
  return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  '''
  Controller for artist page (template/pages/artists.html) of Fyyur with following functions
  - show list of all artists
  - redirect to artist page
  '''
  
  # TODO: replace with real data returned from querying the database
  # query all artist database entries
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  '''
  Controller for artists' search page (template/pages/search_artists.html) of Fyyur with following functions
  - search for artists (get list of results that match the search term)
  - return number of database entries that match the search term
  - redirect to artist page
  '''

  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # get search term from request
  search_term = request.form.get('search_term', '')

  # query database entries of artists that contain the search term
  data = Artist.query.filter(Artist.name.contains(search_term)).all()

  # count query results
  data_count = db.session.query(func.count(Artist.id)).filter(Artist.name.contains(search_term)).all()
  
  # create a dictionary with the results of the search
  response={
    "count": data_count,
    "data": data
    }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  '''
  Controller for the artist page (template/pages/show_artist.html) of Fyyur with following functions
  - shows the artist page with the given artist_id
  - show list of shows (past and upcoming)
  '''

  # TODO: replace with real artist data from the artist table, using artist_id
  # get artist database entry by artist_id
  artist = Artist.query.get(artist_id)

  # get past shows (filter venues by shows containing artist_id and venue_id)
  artist.past_shows = (db.session.query(
    Venue.id.label("venue_id"), 
    Venue.name.label("venue_name"), 
    Venue.image_link.label("venue_image_link"), 
    Show)
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.Venue_id == Venue.id)
    .filter(Show.c.start_time <= datetime.now())
    .all())
  
  # get upcoming shows (filter venues by shows containing artist_id and venue_id)
  artist.upcoming_shows = (db.session.query(
    Venue.id.label("venue_id"), 
    Venue.name.label("venue_name"), 
    Venue.image_link.label("venue_image_link"), 
    Show)
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.Venue_id == Venue.id)
    .filter(Show.c.start_time > datetime.now())
    .all())

  # get number of past shows (filter shows containing artist_id)
  artist.past_shows_count = (db.session.query(
    func.count(Show.c.Artist_id))
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.start_time < datetime.now())
    .all())[0][0]
  
  # get number of upcoming shows (filter shows containing artist_id)
  artist.upcoming_shows_count = (db.session.query(
    func.count(Show.c.Artist_id))
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.start_time > datetime.now())
    .all())[0][0]

  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  '''
  Controller for the edit artist page (template/pages/edit_artist.html) of Fyyur with following functions
  - render ArtistForm with prefilled values
  '''
  # initialize ArtistForm
  form = ArtistForm()

  # get artist database entry
  artist = Artist.query.get(artist_id)

  # prefill form with artist data from query
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link
  form.website_link.data = artist.website_link
  form.image_link.data = artist.image_link
  # form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  '''
  Controller for the edit artist page (template/pages/edit_artist.html) of Fyyur with following functions
  - handle submitted artist data
  - update artist data in database
  - error handling
  '''
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  # get artist data from database by artist_id
  artist = Artist.query.get(artist_id)

  try:
    # get form data to update artist
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    artist.image_link = request.form['image_link']
    artist.website_link = request.form['website_link']
    # artist.seeking_venue = request.form['seeking_venue']
    artist.seeking_description = request.form['seeking_description']

    # add and commit transaction
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    # rollback session in case of error
    db.session.rollback()
    # print error
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally:
    # close session
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  '''
  Controller for the edit venue page (template/pages/edit_venue.html) of Fyyur with following functions
  - handle submitted venue data
  - venue artist data in database
  - error handling
  '''
  # initialize VenueForm
  form = VenueForm()

  # get venue database entry
  venue = Venue.query.get(venue_id)

  # prefill form with venue data from query
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.seeking_description.data = venue.seeking_description
  # form.seeking_talent.data = venue.seeking_talent
  form.website_link.data = venue.website_link
  form.image_link.data = venue.image_link
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  '''
  Controller for the edit artist page (template/pages/edit_venue.html) of Fyyur with following functions
  - handle submitted venue data
  - update venue data in database
  - error handling
  '''

    # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  # get venue data from database by venue_id
  venue = Venue.query.get(venue_id)

  try:
    # get form data to update venue
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.image_link = request.form['image_link']
    # venue.seeking_talent = request.form['seeking_talent']
    venue.seeking_description = request.form['seeking_description']
    venue.website_link = request.form['website_link']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']

    # add and commit transaction
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    # rollback session in case of error
    db.session.rollback()
    # print error
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    # close session
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  '''
  Controller for the create artist page (template/pages/new_artist.html) of Fyyur with following functions
  - render blank ArtistForm
  '''
  # initialize instance of ArtistForm()
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  '''
  Controller for the create artist page (template/pages/new_artist.html) of Fyyur with following functions
  - handle submitted artist data
  - create new artist
  - error handling
  '''

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # initialize instance of ArtistForm()
  form = ArtistForm(request.form)
  
  # validate form input
  if form.validate():
    try:
      # create new artist instance with form data
      newArtist = Artist(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        genres = request.form.getlist('genres'),
        facebook_link = request.form['facebook_link'],
        image_link = request.form['image_link'],
        website_link = request.form['website_link'],
        # seeking_venue = request.form['seeking_venue'],
        seeking_description = request.form['seeking_description']
      )
      # add and commit transaction
      with app.app_context():
        db.session.add(newArtist)
        db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # rollback session in case of error
      db.session.rollback()
      # print error
      print(sys.exc_info())
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    finally:
      # close session
      db.session.close()
  else:
    # flash validation error
    flash(form.errors)
    flash('An error occurred due to form validation. Artist {} could not be listed.'.format(request.form['name']))
  
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  '''
  Controller for the shows page (template/pages/shows.html) of Fyyur with following functions
  - list all shows
  '''
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  # query all shows from association table
  data = (db.session.query(
    Venue.id.label("venue_id"), 
    Venue.name.label("venue_name"),
    Artist.id.label("artist_id"), 
    Artist.name.label("artist_name"), 
    Artist.image_link.label("artist_image_link"), 
    Show)
    .filter(Show.c.Venue_id == Venue.id)
    .filter(Show.c.Artist_id == Artist.id)
    .all())

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  '''
  Controller for the create show page (template/pages/new_show.html) of Fyyur with following functions
  - render blank ShowForm
  '''
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  '''
  Controller for the create show page (template/pages/new_show.html) of Fyyur with following functions
  - handle submitted show data
  - create new show
  - error handling
  '''
  
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # initialize instance of ShowForm()
  form = ShowForm(request.form)
  
  # validate form input
  if form.validate():
    try:
      # create new show instance with form data
      newShow = Show.insert().values(
        Venue_id = request.form['venue_id'],
        Artist_id = request.form['artist_id'],
        start_time = request.form['start_time']
      )
      # execute and commit transaction
      db.session.execute(newShow)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show  was successfully listed!')
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # rollback session in case of error
      db.session.rollback()
      # print error
      print(sys.exc_info())
      flash('An error occurred. Show could not be listed.')
    finally:
      # close session
      db.session.close()
  else:
    # flash validation error
    flash(form.errors)
    flash('An error occurred due to form validation. Show could not be listed.')

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
  '''
  Controller for error page displaying error 404 (not found error)
  '''
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
  '''
  Controller for error page displaying error 500 (server error)
  '''
  return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=app.debug)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

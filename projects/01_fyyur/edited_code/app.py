'''
Python file containing all central components for configuring 
and running the web application Fyyur, i.e.,
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
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for, 
  jsonify
)
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, inspect
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
import sys
from models import db, Venue, Artist, Show
from forms import *
from config import SQLALCHEMY_DATABASE_URI

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# define and configure the app and connect a database object
app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

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
  Converts SQLALchemy collections results (sqlalchemy.util._collections.result) 
  to dictionary

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
  Controller for homepage (template/pages/home.html) of Fyyur with 
  following functions
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
  return render_template(
    'pages/home.html',
    recent_artists = recent_artists,
    recent_venues = recent_venues
  )


#  Venues
#----------------------------------------------------------------------------#

@app.route('/venues')
def venues():
  '''
  Controller for venue page (template/pages/venues.html) of Fyyur with 
  following functions
  - show list of all venues
  - group list by location (city, state)
  - show number 
  '''
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming 
  #       shows per venue.

  # create a list of dictionaries of the cities and states of venues
  data = []
  locations = Venue.query.order_by(Venue.state, Venue.city).all()

  for location in locations:
      location_venues = Venue.query.filter_by(state=location.state).filter_by(city=location.city).all()
      venue = []
      for v in location_venues:
          venue.append({
              'id': v.id,
              'name': v.name,
              'num_upcoming_shows': len(
                  db.session.query(Show).filter(Show.venue_id == v.id).filter(Show.start_time > datetime.now()).all())
          })

      data.append({
          'city': location.city,
          'state': location.state,
          'venues': venue
      })

  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
  '''
  Controller for venues' search page (template/pages/search_venues.html) 
  of Fyyur with following functions
  - search for venues (get list of results that match the search term)
  - return number of database entries that match the search term
  - redirect to venue page
  '''
  # TODO: implement search on venues with partial string search. Ensure it is
  # case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and 
  # "Park Square Live Music & Coffee"
  
  # get search term from request
  search_term = request.form.get('search_term', '')

  # query database entries of venues that contain the search term
  venues = Venue.query.filter(Venue.name.ilike("%" + search_term + "%")).all()

  # create a dictionary with the results of the search
  response={
    "count": len(venues),
    "data": []
  }

  for venue in venues:
    response["data"].append({
        'id': venue.id,
        'name': venue.name,
    })

  return render_template(
    'pages/search_venues.html',
    results=response,
    search_term=search_term
  )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  '''
  Controller for the venue page (template/pages/venues/<int:venue_id>.html) 
  of Fyyur with following functions
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

  past_shows = []
  upcoming_shows = []

  for show in venue.shows:
    temp_show = {
        'artist_id': show.artist_id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    } 
    if show.start_time <= datetime.now():
        past_shows.append(temp_show)
    else:
        upcoming_shows.append(temp_show)

  # object class to dict
  data = vars(venue)

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  '''
  Controller for the create venue page (template/pages/venues/create.html) 
  of Fyyur with following functions
  - show blank create venue form
  '''
  # initialize VenueForm
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  '''
  Controller for the create venue page (template/pages/venues/create.html) 
  of Fyyur with following functions
  - handle submitted venue data
  - create new venue
  - error handling
  '''

  # TODO: insert form data as a new Venue record in the db, instead
  # create form for request venue data
  form = VenueForm(request.form, meta={'csrf': False})

  # TODO: modify data to be the data object returned from db insertion
  # validate form input
  if form.validate():
    try:
      # create new venue instance with form data
      newVenue = Venue(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        address = form.address.data,
        phone = form.phone.data,
        image_link = form.image_link.data,
        seeking_talent= True if 'seeking_talent' in request.form else False,
        seeking_description = form.seeking_description.data,
        website_link = form.website_link.data,
        genres = form.genres.data,
        facebook_link = form.facebook_link.data)

      # add and commit transaction
      with app.app_context():
        db.session.add(newVenue)
        db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + form.name.data + ' was successfully listed!')
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # rollback session in case of error
      db.session.rollback()
      # print error
      print(sys.exc_info())
      flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    finally:
      # close session
      db.session.close()
  else:
    # flash validation error
    flash(form.errors)
    flash('An error occurred due to form validation. Venue {} could not be listed.'.format(form.name.data))

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  '''
  Controller for the delete venue page (template/pages/venues/<venue_id>.html) 
  of Fyyur with following functions
  - delete existing venue database entry
  - error handling
  '''
  
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session 
  # commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, 
  # have it so that clicking that button delete it from the db then redirect 
  # the user to the homepage

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
#----------------------------------------------------------------------------#
@app.route('/artists')
def artists():
  '''
  Controller for artist page (template/pages/artists.html) of Fyyur with 
  following functions
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
  Controller for artists' search page (template/pages/search_artists.html) 
  of Fyyur with following functions
  - search for artists (get list of results that match the search term)
  - return number of database entries that match the search term
  - redirect to artist page
  '''

  # TODO: implement search on artists with partial string search. Ensure 
  # it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and 
  # "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  # get search term from request
  search_term = request.form.get('search_term', '')

  # query database entries of artists that contain the search term
  artists = Artist.query.filter(Artist.name.ilike("%" + search_term + "%")).all()

  # create a dictionary with the results of the search
  response={
    "count": len(artists),
    "data": []
  }

  for artist in artists:
    response["data"].append({
        'id': artist.id,
        'name': artist.name,
    })
  
  return render_template(
    'pages/search_venues.html',
    results=response,
    search_term=search_term
  )

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  '''
  Controller for the artist page (template/pages/show_artist.html) 
  of Fyyur with following functions
  - shows the artist page with the given artist_id
  - show list of shows (past and upcoming)
  '''

  # TODO: replace with real artist data from the artist table, using artist_id
  # get artist database entry by artist_id
  artist = Artist.query.get(artist_id)

  # get past shows (filter venues by shows containing artist_id and venue_id)
  past_shows = []
  upcoming_shows = []

  for show in artist.shows:
    temp_show = {
        'venue_id': show.venue_id,
        'venue_name': show.venue.name,
        'venue_image_link': show.venue.image_link,
        'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
    } 
    if show.start_time <= datetime.now():
        past_shows.append(temp_show)
    else:
        upcoming_shows.append(temp_show)

  # object class to dict
  data = vars(artist)

  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)

#  Update
#----------------------------------------------------------------------------#
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  '''
  Controller for the edit artist page (template/pages/edit_artist.html) 
  of Fyyur with following functions
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
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  '''
  Controller for the edit artist page (template/pages/edit_artist.html) 
  of Fyyur with following functions
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
    artist.seeking_venue = True if 'seeking_venue' in request.form else False
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
  Controller for the edit venue page (template/pages/edit_venue.html) 
  of Fyyur with following functions
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
  form.seeking_talent.data = venue.seeking_talent
  form.website_link.data = venue.website_link
  form.image_link.data = venue.image_link
  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  '''
  Controller for the edit artist page (template/pages/edit_venue.html) 
  of Fyyur with following functions
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
    venue.seeking_talent = True if 'seeking_talent' in request.form else False
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
#----------------------------------------------------------------------------#

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  '''
  Controller for the create artist page (template/pages/new_artist.html) 
  of Fyyur with following functions
  - render blank ArtistForm
  '''
  # initialize instance of ArtistForm()
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  '''
  Controller for the create artist page (template/pages/new_artist.html) 
  of Fyyur with following functions
  - handle submitted artist data
  - create new artist
  - error handling
  '''

  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  # initialize instance of ArtistForm()
  form = ArtistForm(request.form, meta={"csrf": False})
  
  # validate form input
  if form.validate():
    try:
      # create new artist instance with form data
      newArtist = Artist(
        name = form.name.data,
        city = form.city.data,
        state = form.state.data,
        phone = form.phone.data,
        genres = form.genres.data,
        facebook_link = form.facebook_link.data,
        image_link = form.image_link.data,
        website_link = form.website_link.data,
        seeking_venue = True if "seeking_venue" in request.form else False,
        seeking_description = form.seeking_description.data
      )
      # add and commit transaction
      with app.app_context():
        db.session.add(newArtist)
        db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + form.name.data + ' was successfully listed!')
    except:
      # TODO: on unsuccessful db insert, flash an error instead.
      # rollback session in case of error
      db.session.rollback()
      # print error
      print(sys.exc_info())
      flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    finally:
      # close session
      db.session.close()
  else:
    # flash validation error
    flash(form.errors)
    flash('An error occurred due to form validation. Artist {} could not be listed.'.format(form.name.data))
  
  return render_template('pages/home.html')

#  Shows
#----------------------------------------------------------------------------#

@app.route('/shows')
def shows():
  '''
  Controller for the shows page (template/pages/shows.html) 
  of Fyyur with following functions
  - list all shows
  '''
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  # query all shows and append elements to array
  data = []
  shows = db.session.query(Show).join(Artist).join(Venue).all()
  for show in shows:
    data.append({
    "venue_id" : show.venue_id,
    "venue_name" : show.venue.name,
    "artist_id" : show.artist_id,
    "artist_image_link" : show.artist.image_link,
    "artist_name" : show.artist.name,
    "start_time" : show.start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  '''
  Controller for the create show page (template/pages/new_show.html) 
  of Fyyur with following functions
  - render blank ShowForm
  '''
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  '''
  Controller for the create show page (template/pages/new_show.html) 
  of Fyyur with following functions
  - handle submitted show data
  - create new show
  - error handling
  '''
  
  # called to create new shows in the db, 
  # upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # initialize instance of ShowForm()
  form = ShowForm(request.form, meta={"csrf": False})
  
  # validate form input
  if form.validate():
    try:
      # create new show instance with form data
      newShow = Show(
        venue_id = form.venue_id.data,
        artist_id = form.artist_id.data,
        start_time = form.start_time.data
      )
      # execute and commit transaction
      with app.app_context():
        db.session.add(newShow)
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
        Formatter(
          '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
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

#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import click
from flask.cli import with_appcontext

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Run this command to clear all Artist, Venue and Show records from your db
#----------------------------------------------------------------------------#

@click.command(name='delete_all')
@with_appcontext
def delete_all():
  Artist.query.delete()
  Venue.query.delete()
  db.session.commit()

app.cli.add_command(delete_all)

#----------------------------------------------------------------------------#
# Run this command to seed database with fake data
#----------------------------------------------------------------------------#

@click.command(name='create_all')
@with_appcontext
def create_all():
  artists_and_venues = [
    Artist(
      name='Guns N Petals',
      city='San Francisco',
      state='CA',
      phone='326-123-5000',
      genres=['Rock n Roll'],
      website='https://www.gunsnpetalsband.com',
      facebook_link='https://www.facebook.com/GunsNPetals',
      seeking_venue=True,
      seeking_description='Looking for shows to perform at in the San Francisco Bay Area!',
      image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
    ),
    Artist(
      name='Matt Quevedo',
      city='New York',
      state='NY',
      phone='300-400-5000',
      genres=['Jazz'],
      facebook_link='https://www.facebook.com/mattquevedo923251523',
      seeking_venue=False,
      image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
    ),
    Artist(
      name='The Wild Sax Band',
      city='San Francisco',
      state='CA',
      phone='432-325-5432',
      genres=['Jazz', 'Classical'],
      seeking_venue=False,
      image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
    ),
    Venue(
      name='The Musical Hop',
      address='1015 Folsom Street',
      city='San Francisco',
      state='CA',
      phone='123-123-1234',
      genres=['Jazz', 'Reggae', 'Swing', 'Classical', 'Folk'],
      website='https://www.themusicalhop.com',
      facebook_link='https://www.facebook.com/TheMusicalHop',
      seeking_talent=True,
      seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.',
      image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    ),
    Venue(
      name='The Dueling Pianos Bar',
      address='335 Delancey Street',
      city='New York',
      state='NY',
      phone='914-003-1132',
      genres=['Classical', 'R&B', 'Hip-Hop'],
      website='https://www.theduelingpianos.com',
      facebook_link='https://www.facebook.com/theduelingpianos',
      seeking_talent=False,
      image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
    ),
    Venue(
      name='Park Square Live Music & Coffee',
      address='34 Whiskey Moore Ave',
      city='San Francisco',
      state='CA',
      phone='415-000-1234',
      genres=['Rock n Roll', 'Jazz', 'Classical', 'Folk'],
      website='https://www.parksquarelivemusicandcoffee.com',
      facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
      seeking_talent=False,
      image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    ),
  ]

  db.session.add_all(artists_and_venues)
  db.session.commit()

  guns_n_petals = Artist.query.filter_by(name='Guns N Petals').first()
  matt_quevedo = Artist.query.filter_by(name='Matt Quevedo').first()
  the_wild_sax_band = Artist.query.filter_by(name='The Wild Sax Band').first()
  the_musical_hop = Venue.query.filter_by(name='The Musical Hop').first()
  park_square_live_music_coffee = Venue.query.filter_by(name='Park Square Live Music & Coffee').first()

  shows = [
    Show(
      start_time='2019-05-21T21:30:00.000Z',
      artist=guns_n_petals,
      venue=the_musical_hop,
    ),
    Show(
      start_time='2019-06-15T23:00:00.000Z',
      artist=matt_quevedo,
      venue=park_square_live_music_coffee,
    ),
    Show(
      start_time='2035-04-01T20:00:00.000Z',
      artist=the_wild_sax_band,
      venue=park_square_live_music_coffee,
    ),
    Show(
      start_time='2035-04-08T20:00:00.000Z',
      artist=the_wild_sax_band,
      venue=park_square_live_music_coffee,
    ),
    Show(
      start_time='2035-04-15T20:00:00.000Z',
      artist=the_wild_sax_band,
      venue=park_square_live_music_coffee,
    ),
  ]

  db.session.add_all(shows)
  db.session.commit()

app.cli.add_command(create_all)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.Text)
    shows = db.relationship('Show', backref='venue', cascade='save-update, merge, delete', lazy=True)

    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.Text)
    shows = db.relationship('Show', backref='artist', cascade='save-update, merge, delete', lazy=True)

    def __repr__(self):
      return f'<Artist {self.id} {self.name}>'

class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
      return f'<Show {self.id} {self.start_time}>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if not isinstance(value, str):
    value = value.strftime("%m/%d/%Y, %H:%M:%S")

  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues_by_location = []
  for city_state in Venue.query.distinct(Venue.city, Venue.city):
    venues_for_location = []

    for venue in Venue.query.filter(Venue.city == city_state.city, Venue.state == city_state.state).all():
      num_upcoming_shows = Show.query.join(Venue).filter(Venue.id == venue.id, Show.start_time >= datetime.now()).count()

      venues_for_location.append(
        {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows,
        }
      )

    venues_by_location.append(
      {
        "city": city_state.city,
        "state": city_state.state,
        "venues": venues_for_location,
      }
    )

  return render_template('pages/venues.html', areas=venues_by_location);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  venues = db.session.query(Venue.id, Venue.name).filter(Venue.name.ilike('%{}%'.format(request.form['search_term']))).all()
  venues_results = []

  if venues:
    for venue in venues:
      num_upcoming_shows = Show.query.join(Venue).filter(Venue.id == venue.id, Show.start_time >= datetime.now()).count()
      venues_results.append(
        {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows,
        }
      )

  response={
    "count": len(venues),
    "data": venues_results,
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get(venue_id)

  if venue:
    venue_dict = venue.__dict__
    venue_dict["upcoming_shows"] = db.session.query(Show.start_time, Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link')).join(Venue, Artist).filter(Venue.id == venue_dict["id"], Show.start_time >= datetime.now()).all()
    venue_dict["past_shows"] = db.session.query(Show.start_time, Artist.id.label('artist_id'), Artist.name.label('artist_name'), Artist.image_link.label('artist_image_link')).join(Venue, Artist).filter(Venue.id == venue_dict["id"], Show.start_time < datetime.now()).all()
    venue_dict["past_shows_count"] = len(venue_dict["past_shows"])
    venue_dict["upcoming_shows_count"] = len(venue_dict["upcoming_shows"])

    return render_template('pages/show_venue.html', venue=venue_dict)
  else:
    flash("This venue doesn't exist, please pick a venue from this list", 'alert-warning')
    return redirect(url_for('venues'))

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    venue = Venue(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      address=request.form['address'],
      city=request.form['city'],
      state= request.form['state'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link'],
    )

    db.session.add(venue)
    db.session.commit()
    venue_name = venue.name
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    form = VenueForm()
    flash('An error occurred. Venue ' + venue_name + ' could not be listed.', 'alert-danger')
    return render_template('forms/new_venue.html', form=form)
  else:
    flash('Venue ' + venue_name + ' was successfully listed!', 'alert-success')
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  error = False
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    venue_name = venue.name
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    flash("An error occured, this venue couldn't be deleted", 'alert-danger')
    return redirect(url_for('show_venue', venue_id=venue_id))
  else:
    flash('Venue ' + venue_name + ' was successfully deleted!', 'alert-success')
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = db.session.query(Artist.id, Artist.name).all()
  artists_results = []

  for artist in artists:
    num_upcoming_shows = Show.query.join(Artist).filter(Artist.id == artist.id, Show.start_time >= datetime.now()).count()
    artists_results.append(
      {
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": num_upcoming_shows,
      }
    )

  return render_template('pages/artists.html', artists=artists_results)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artists = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike('%{}%'.format(request.form['search_term']))).all()
  artists_results = []

  if artists:
    for artist in artists:
      num_upcoming_shows = Show.query.join(Artist).filter(Artist.id == artist.id, Show.start_time >= datetime.now()).count()
      artists_results.append(
        {
          "id": artist.id,
          "name": artist.name,
          "num_upcoming_shows": num_upcoming_shows,
        }
      )

  response={
    "count": len(artists),
    "data": artists_results,
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)

  if artist:
    artist_dict = artist.__dict__
    artist_dict["upcoming_shows"] = db.session.query(Show.start_time, Venue.id.label('venue_id'), Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link')).join(Venue, Artist).filter(Artist.id == artist_dict["id"], Show.start_time >= datetime.now()).all()
    artist_dict["past_shows"] = db.session.query(Show.start_time, Venue.id.label('venue_id'), Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link')).join(Venue, Artist).filter(Artist.id == artist_dict["id"], Show.start_time < datetime.now()).all()
    artist_dict["past_shows_count"] = len(artist_dict["past_shows"])
    artist_dict["upcoming_shows_count"] = len(artist_dict["upcoming_shows"])

    return render_template('pages/show_artist.html', artist=artist_dict)
  else:
    flash("This artist doesn't exist, please pick an artist from this list", 'alert-warning')
    return redirect(url_for('artists'))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  error = False
  try:
    artist = Artist(
      name=request.form['name'],
      genres=request.form.getlist('genres'),
      city=request.form['city'],
      state= request.form['state'],
      phone=request.form['phone'],
      facebook_link=request.form['facebook_link'],
    )

    db.session.add(artist)
    db.session.commit()
    artist_name = artist.name
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    form = ArtistForm()
    flash('An error occurred. Artist ' + artist_name + ' could not be listed.', 'alert-danger')
    return render_template('forms/new_artist.html', form=form)
  else:
    flash('Artist ' + artist_name + ' was successfully listed!', 'alert-success')
    return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = db.session.query(
    Show.start_time,
    Artist.id.label('artist_id'),
    Artist.name.label('artist_name'),
    Artist.image_link.label('artist_image_link'),
    Venue.id.label('venue_id'),
    Venue.name.label('venue_name'),
  ).join(Venue, Artist).all()

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  error = False
  try:
    show = Show(
      start_time=request.form['start_time'],
      artist_id=request.form['artist_id'],
      venue_id=request.form['venue_id'],
    )

    db.session.add(show)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    form = ShowForm()
    flash('An error occurred. Show could not be listed.', 'alert-danger')
    return render_template('forms/new_show.html', form=form)
  else:
    flash('Show was successfully listed!', 'alert-success')
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

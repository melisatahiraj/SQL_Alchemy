# Import the dependencies.
from flask import Flask, jsonify

import numpy as np
import datetime as dt
import sqlalchemy


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def main():
    """List all available routes."""

    return (
        f"Welcome to the Hawaii Weather App!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation - Precipitation Route<br/>"
        f"/api/v1.0/stations - Stations Route<br/>"
        f"/api/v1.0/tobs - Temperature Observations Route<br/>"
        f"/api/v1.0/start - Start Date Route<br/>"
        f"/api/v1.0/start/end - Start/End Date Route<br/>"
    )

#-------------------------------------------------

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of precipitation analysis for the last 12 months (date & prcp)"""

    # Query through precipitation data
    prcp_results = session.query(Measurement.date, Measurement.prcp).all()

    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of precipitation values
    prcp_values = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_values.append(prcp_dict)

    return jsonify(prcp_values)

#-------------------------------------------------

@app.route("/api/v1.0/stations")
def station():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of stations data"""

    # Query through station data
    station_results = session.query(Station.station, Station.id, Station.name).all()

    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of station values
    station_values = []
    for station, id, name in station_results:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["ID"] = id
        station_dict["Name"] = name
        station_values.append(station_dict)

    return jsonify(station_values)

#-------------------------------------------------

@app.route("/api/v1.0/tobs")
def tobs():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of temperature observations data for the previous year"""

    # Query through temperature observation data
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.station == 'USC00519281').\
                    filter(Measurement.date >= '2016-08-23').\
                    order_by(Measurement.date).all()

    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of temperature observation values
    tobs_values = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temperature"] = tobs
        tobs_values.append(tobs_dict)

    return jsonify(tobs_values)

#-------------------------------------------------

@app.route("/api/v1.0/<start>")
def start_date(start):
    
    start = dt.date(2010, 1, 1)

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of minimum, average, and maximum temperature observations for the specified start date"""

    # Query through starting dates data
    start_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                    filter(Measurement.date >= start).all()
    
    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of starting date values
    start_values = []
    for date, min, avg, max in start_date:
        start_dict = {}
        start_dict["Date"] = date
        start_dict["Min"] = min
        start_dict["Average"] = avg
        start_dict["Max"] = max
        start_values.append(start_dict)

    return jsonify(start_values)

#-------------------------------------------------

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    start = dt.date(2010, 1, 1)
    end = dt.date(2017, 8, 23)
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return list of minimum, average, and maximum temperature observations for the specified start and end date"""

    # Query through starting and ending dates data
    start_end_date = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    # Close session
    session.close()

    # Create a dictionary from the row data and append to a list of of starting and ending date values
    start_end_values = []
    for min, avg, max in start_end_date:
        start_end_dict = {}
        start_end_dict["Min"] = min
        start_end_dict["Average"] = avg
        start_end_dict["Max"] = max
        start_end_values.append(start_end_dict)

    return jsonify(start_end_values)


if __name__ == '__main__':
    app.run(debug=True)
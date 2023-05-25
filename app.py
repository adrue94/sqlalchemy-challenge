# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
# session = Session(engine), but maybe per-function?

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Welcome to my API! <br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/station <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end <br/> <br/>"
        f"Please note start and end endpoints only accepts YYYY format <br/> <i>(e.g., /api/v1.0/2011/2014)</i>"
    )

###############
#Precipitation#
###############
# Returns json with the date as the key and the value as the precipitation 
# Only returns the jsonified precipitation data for the last year in the database 

@app.route("/api/v1.0/precipitation")
def precipitations():
    import datetime as dt
    session = Session(engine)

    """Returning query results from last 12 months of precipitation analysis"""
    # Querying analysis
    date = dt.datetime(2016, 8, 23)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > date).all()
    session.close()

    # Creating dictionary
    precipitationData = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp 
        precipitationData.append(precipitation_dict)
    return jsonify(precipitationData)

###############
####Station####
###############
# Returns jsonified data of all of the stations in the database (3 points)
# As dict? As list? 

@app.route("/api/v1.0/station")
def stations():
    session = Session(engine)

    """Returning data of all stations in database"""
    # Querying stations
    stationRes = session.query(station.name, station.station).all()
    session.close()

    # Creating list
    stationData = []
    for name, id in stationRes:
        station_dict = {}
        station_dict["Name"] = name
        station_dict['ID'] = id
        stationData.append(station_dict) 
    return jsonify(stationData)
    # allStations = list(np.ravel(stationRes))
    # return jsonify(allStations)
    # # Querying stations
    # stationRes = session.query(station.name).all()
    # session.close()

    # # Creating list
    # allStations = list(np.ravel(stationRes))
    # return jsonify(allStations)

###############
#####TOBS######
###############
# Returns jsonified data for the most active station (USC00519281) 
# Only returns the jsonified data for the last year of data 

@app.route("/api/v1.0/tobs")
def tobs():
    import datetime as dt
    session = Session(engine)

    """Returning query results from last 12 months of TOBS analysis from USC00519281"""
    # Querying analysis
    date = dt.datetime(2016, 8, 23)
    tobsRes = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > date).\
        filter(measurement.station == 'USC00519281').all()
    session.close()

    # Creating dictionary
    tobsData = []
    for date, tobs in tobsRes:
        tobs_dict = {}
        tobs_dict[date] = tobs 
        tobsData.append(tobs_dict)
    return jsonify(tobsData)

###############
#####START#####
###############
# Returns jsonified data from start date


@app.route("/api/v1.0/<start>")
def startDate(start):
    import datetime as dt
    session = Session(engine)
    """Fetch the data based on start date"""

    DateQuery = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(func.strftime("%Y"), measurement.date > start).all()
    session.close()

    # Creating dict
    DateData = []
    for tmin, tavg, tmax in DateQuery:
        DateDict = {}
        DateDict["Min Temp"] = tmin 
        DateDict["Avg Temp"] = tavg
        DateDict["Max Temp"] = tmax
        DateData.append(DateDict)

    return jsonify(DateData)

###############
######END######
###############
# Returns jsonified data from start to end date
# Should we provide error for when search fails?

@app.route("/api/v1.0/<start>/<end>")
def stEndDate(start, end):
    import datetime as dt
    session = Session(engine)
    """Fetch the data based on start date"""

    DateQuery = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(func.strftime("%Y"), measurement.date > start).\
        filter(func.strftime("%Y"), measurement.date < end).all()
    session.close()

    # Creating dict
    DateData = []
    for tmin, tavg, tmax in DateQuery:
        DateDict = {}
        DateDict["Min Temp"] = tmin 
        DateDict["Avg Temp"] = tavg
        DateDict["Max Temp"] = tmax
        DateData.append(DateDict)

    return jsonify(DateData)

#################################################
# Define main behaviour (Whatever that means)
#################################################
if __name__ == "__main__":
    app.run(debug=True)

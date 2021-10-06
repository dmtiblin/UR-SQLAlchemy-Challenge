# import dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

# Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement



#################################################
# Flask Routes
#################################################

#  Define what to do when a user hits the homepage / index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return ("Welcome to my 'Home' page! <br/>"
            "Here is a list of the available routes <br/>"
            "/api/v1.0/precipitation <br/>"
            "/api/v1.0/stations <br/>"
            "/api/v1.0/tobs <br/>"
            "/api/v1.0/<start> <br/>"
            "/api/v1.0/<start>/<end> <br/>"
            )


#Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def about():
    print("Server received request for 'About' page...")
    return ("Welcome to my 'About' page!")


#Define what to do when a user hits the /api/v1.0/stations route
  #Return the JSON representation of your dictionary
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #query list of stations 
    results = session.query(Station.station, Station.name).all()
    session.close()
     
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

###################################################################
 #Define what to do when a user hits the /api/v1.0/tobs route    
@app.route("/api/v1.0/tobs")
def tobs():
  
    #Query the dates and temperature observations of the most active station for the last year of data
    session = Session(engine)
    active_results = session.query(Measurement.station, func.count(Measurement.prcp)).group_by(Measurement.station).order_by(func.count(Measurement.prcp).desc())
    date_filter = (func.strftime('%Y-%m-%d', Measurement.date) < dt.datetime(2017,8,23)) & (func.strftime('%Y-%m-%d', Measurement.date) > dt.datetime(2016,8,23))
    tobs_results = session.query(func.strftime('%Y-%m-%d',Measurement.date), Measurement.tobs).filter(date_filter).filter_by(station = id)

    session.close()

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_results_rows = [{"Date": result[0], "TOBS": result[1]} for result in tobs_results]
    return jsonify(tobs_results_rows)



if __name__ == '__main__':
    app.run(debug=True)

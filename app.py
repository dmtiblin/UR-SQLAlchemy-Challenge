
# import dependencies
from flask import Flask, jsonify, render_template, request
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime 

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
def index():
    
            
    urls = [
            "/api/v1.0/precipitation",
            "/api/v1.0/stations",
            "/api/v1.0/tobs",
            "/api/v1.0/<start>",
            "/api/v1.0/<start>/<end>"
            ]  
    return render_template('index.html', title='Welcome', urls = urls)
####################################################################

#Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results to a dictionary using date as the key and prcp as the value.
    session = Session(engine)
    #query list of stations 
    results = session.query(Measurement).all()
    session.close()

    all_prcp= []
    for measurement in results:
        prcp_dict = {measurement.date : measurement.prcp }
        all_prcp.append(prcp_dict)

    #Return the JSON representation of your dictionary.
    return jsonify(all_prcp)

##############################################################################

#Define what to do when a user hits the /api/v1.0/stations route
  
@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
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
    id = active_results[0][0]
    date_filter = (func.strftime('%Y-%m-%d', Measurement.date) < datetime.datetime(2017,8,23)) & (func.strftime('%Y-%m-%d', Measurement.date) > datetime.datetime(2016,8,23))
    tobs_results = session.query(func.strftime('%Y-%m-%d',Measurement.date), Measurement.tobs).filter(date_filter).filter_by(station = id)

    session.close()

    #Return a JSON list of temperature observations (TOBS) for the previous year.
    tobs_results_rows = [{"Date": result[0], "TOBS": result[1]} for result in tobs_results]
    return jsonify(tobs_results_rows)
   
###########################################################

@app.route("/api/v1.0/<start>")
def start(start):
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
    #(calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date)
    #Route accepts the start date as a parameter from the URL
    #convert the route input YYYY-MM-DD into date using datetime
    
    date = datetime.datetime.strptime(start, "%Y-%m-%d")
    session = Session(engine)
 
    session.close()
    
    lowest_temp = session.query(func.min(Measurement.tobs)).filter((Measurement.date > date))
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > date)
    avg_temp =session.query(func.avg(Measurement.tobs)).filter(Measurement.date > date)

    print ("lowest temp, highest temp, average temp")
    return jsonify (lowest_temp[0],max_temp[0], avg_temp[0])

#################################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    ##Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end date range
    #(calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive)
    #Route accepts the start and end dates as parameters from the URL
    date1 = datetime.datetime.strptime(start, "%Y-%m-%d")
    date2 = datetime.datetime.strptime(end, "%Y-%m-%d")
    session = Session(engine)
 
    session.close()
    
    lowest_temp = session.query(func.min(Measurement.tobs)).filter((Measurement.date >= date1) & (Measurement.date <= date2))
    max_temp = session.query(func.max(Measurement.tobs)).filter((Measurement.date >= date1) & (Measurement.date <= date2))
    avg_temp =session.query(func.avg(Measurement.tobs)).filter((Measurement.date >= date1) & (Measurement.date <= date2))

    print ("lowest temp, highest temp, average temp")
    return jsonify (lowest_temp[0],max_temp[0], avg_temp[0])







if __name__ == '__main__':
    app.run(debug=True)

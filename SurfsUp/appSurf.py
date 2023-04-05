# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
ME = Base.classes.measurement
ST = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# establishes the home route for the server
@app.route("/")
def home():
    #List all available api routes
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )



# flask route for /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Return the precipitation data for the last year
    # Calculate the date 1 year ago from the last data point in the database
    recentDate = session.query(ME.date).order_by(ME.date.desc()).first()
    lastTwelve = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    scores = session.query(ME.date, ME.prcp)\
                    .filter(ME.date >= lastTwelve).order_by(ME.date).all()


    # Convert query results to a dictionary
    prcp_dict = dict(scores)

    # jsonify results
    return jsonify(prcp_dict)



# flask route for /api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    #Return a list of stations for the last year
    # Query all stations
    all_stations = session.query(ST.station).all()

    # Convert list of tuples into normal list
    stations = list(np.ravel(all_stations))

    # jsonify
    return jsonify(stations)



# flask route for /api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    #Query the dates and temperature observations of the most-active station for the previous year of data.
    activeTwelve = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the last 12 months of temperature data for the most active station
    results = session.query(ME.date, ME.tobs).\
        filter(ME.station == 'USC00519281').\
        filter(ME.date >= activeTwelve).all()

    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(results))

    # jsonify
    return jsonify(temps)


# flask route for /api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    
     # Query the minimum, average, and maximum temperature for the specified date range
    summary_stats = [func.min(ME.tobs), func.max(ME.tobs), func.avg(ME.tobs)]

     # Convert the start and end dates to datetime objects
    if not end:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')

        mostActive_results = session.query(*summary_stats).filter(ME.date >= start_date).all()

        temp_list = list(np.ravel(mostActive_results))

        # jsonify
        return jsonify(temp_list)
    
                                                            
    else:

        start_date = dt.datetime.strptime(start, '%Y-%m-%d')

        end_date = dt.datetime.strptime(end, '%Y-%m-%d')

        mostActive_results = session.query(*summary_stats)\
                                .filter(ME.date >= start_date)\
                                .filter(ME.data <= end_date).all()
    
    # Create a dictionary from the row data and append to a list of all_temps
    all_temps_list = list(np.ravel(mostActive_results))

    # Return the JSON representation of the list
    return jsonify(all_temps_list)

# app launcher
if __name__ == "__main__":
    app.run(debug=True) 
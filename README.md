# sqlalchemy-challenge
module 10 assignment

used '03-Stu_Dow_Dates' in the 10 folder for reference
used '02-Stu_Sunny_Hours' in the 09 folder for reference
used 'Dr. A module 10 youtube video' to fix the last portion of my code 

Used the following dependicies to create climate analysis and data exploration : 
    from flask import Flask, jsonify
    import numpy as np
    import datetime as dt
    import pandas as pd
    import sqlalchemy
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine, func

created DB set-up
Reflected DB and tables
created references for each table
created session like from python 
created Flask set-up and environment

created routes for:
        /api/v1.0/precipitation<br/>"
        /api/v1.0/stations<br/>"
        /api/v1.0/tobs<br/>"
        /api/v1.0/start<br/>"
        /api/v1.0/start/end"

all routes consisted on same code: starting with defining, a query, convert list to tuples, and return jsonified list.

For: /api/v1.0/start/end"
required different parameters with conditions, a start and end to datetime objects.

created app launcher
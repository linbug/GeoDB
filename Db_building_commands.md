
##Make the database and enable postgis functionality
createdb nasa

pgcli nasa

CREATE SCHEMA rainfall;

CREATE EXTENSION postgis;

CREATE EXTENSION postgis_topology;

##Converting all the files into the sql rasters
http://postgis.net/docs/manual-2.2/using_raster_dataman.html

raster2pgsql -c -C -s 4326 -n forecast_date *.tiff -t 50x50 rainfall.rasters > rainfall_all_Jan18.sql

-c                  *--Create new table and populate it with raster(s), this is the default mode.*

-C                  *--Apply raster constraints -- srid, pixelsize etc. to ensure raster is properly registered in raster_columns view.*

-s 4326             *--Assign output raster with specified SRID. NASA rainfall data is WGS8*

-n forecast_date    *--Assign the forecast date to a new column called 'forecast_date'*

-t 50x50            *--tile the data in 50x50px blocks--*


file *.tiff | grep -v TIFF | cut -c 1-8  <!-- finds files that are not in the correct format -->

psql -d nasaJan18 -f rainfall_allJan18.sql

##Querying the database

nasa> CREATE INDEX gist_index on rainfall.rasters using gist (ST_ConvexHull(rast)); --create a Gist index for the data

nasa> select * from rainfall.rasters limit 3;

nasa> select st_nearestvalue(rast, ST_GEOMFromtext('POINT(-81.233 42.983)',4326)) from rainfall.rasters;
--this returns a range of values

nasa>select st_nearestvalue(rast, ST_GEOMFromtext('POINT(0 51)',4326)), forecast_date from rainfall.rasters;
--this returns a column of all 255

nasa> SELECT forecast_date, st_nearestvalue(rast, ST_geomfromtext('Point(40 -72)', 4
           326)) from rainfall.rasters where forecast_date >= '2014-12-17' and forecast_d
           ate <= '2014-12-24' and st_intersects(rast, st_geomfromtext('Point(40 -72)',
           4326)); --use the gist index

--------------------------------------------

##

>>>%run app/__init__.py

>>>day1 = Nasa.query.filter_by(rid=1).first()

>>>

--------------------------------------------

>>> import psycopg2
>>> conn = psycopg2.connect("dbname = 'nasa'")
>>> cur = conn.cursor()
>>> cur.execute("""SELECT rid FROM rainfall.rasters where rid=1""")
>>> rows = cur.fetchall()

---------------------------------------------

Notes:

The TRMM data only extends from
lat: -50 to 50 [null = 9999]
long: -179 to 180 [null = -3.40282e+38]



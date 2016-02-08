
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

nasa> SELECT forecast_date, st_nearestvalue(rast, ST_geomfromtext('Point(40 51)', 4
           326)) from rainfall.rasters where forecast_date >= '2014-12-17' and forecast_d
           ate <= '2014-12-24' and st_intersects(rast, st_geomfromtext('Point(40 -72)',
           4326)); --use the gist index

nasa> --this eliminates the black areas so I don't get nulls in the returned values--
select forecast_date from rainfall.rasters where forecast_date >= '1999-11-17' and forecast_date <= '1999-12-24' and st_intersects(rast, ST_GEOMFromtext('Point(0 0)',4326)) and not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 50)'),st_geomfromtext('Point(180 90)'))) and not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 -90)'),st_geomfromtext('Point(180 -50)'))) order by forecast_date;

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
long: -180 to 180 [null = -3.40282e+38]

---------------------------------------------
AWS:
Getting into Ubuntu
ssh -i ~/oath/to/pem ubuntu@52.34.140.34

Getting into the database:
psql -h linbug-geo.cohzeuit6v5y.us-west-2.rds.amazonaws.com -U linbug_geo linbug_geo

---------------------------------------------
Troubleshooting why I was getting duplicate values for some of the locations:
e.g. this query returns 2 values per day:

select st_nearestvalue(rast, ST_GEOMFromtext('POINT(-72 40)',4326)), forecast_date from rainfall.rasters where forecast_date >= '1999-11-17' and forecast_date <= '1999-12-24' and st_intersects(rast, ST_GEOMFromtext('Point(-72 40)',4326)) order by forecast_date;

So we tried:

--just show the number of rows for each forecast date between a date range--
select forecast_date, count(forecast_date)
from rainfall.rasters
where forecast_date >= '1999-11-17'
and forecast_date <= '1999-12-24'
and st_intersects(rast, ST_GEOMFromtext('Point(-72 40)',4326))
group by forecast_date;

--count the number of values for each date. There were 435, which probably means that there are 435 rasters
select forecast_date, count(forecast_date)
from rainfall.rasters
group by forecast_date
having count(forecast_date) != 1;

--
select count(*)
from rainfall.rasters
group by forecast_date
having count(forecast_date) != 1;

--eliminate any tiles that intersect with the null box at the top of the map--
select forecast_date, count(forecast_date)
from rainfall.rasters
where forecast_date >= '1999-11-17'
and forecast_date <= '1999-12-24'
and st_intersects(rast, ST_GEOMFromtext('Point(0 0)',4326))
and not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 50)'),st_geomfromtext('Point(180 90)')));

--as above, order by forecast_date--
select forecast_date
from rainfall.rasters
where forecast_date >= '1999-11-17'
and forecast_date <= '1999-12-24'
and st_intersects(rast, ST_GEOMFromtext('Point(0 0)',4326))
and not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 50)'),st_geomfromtext('Point(180 90)')))
order by forecast_date;

--as above with counts. There was only one row per date--
select count(forecast_date)
from rainfall.rasters where forecast_date >= '1999-11-17'
and forecast_date <= '1999-12-24'
and st_intersects(rast, ST_GEOMFromtext('Point(0 0)',4326))
and not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 50)'),st_geomfromtext('Point(180 90)')))
group by forecast_date;




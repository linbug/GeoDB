#PostgreSQL with PostGIS

Getting NASA data into a PostGIS database, and querying it.

1. Download NASA data in GeoTIFF format
    - need to build a web scraper that will automate this
    - is there some advantage to TIFF vs GeoTIFF?

2. Make a database in pgsql that has postgis functionality enabled:
 [install](http://postgis.net/install/)

 $ createdb gisdb
 $ pgcli gisdb -- opens gisdb in repl
 gisdb> -- Enable PostGIS (includes raster)
        CREATE EXTENSION postgis;
        -- Enable Topology
        CREATE EXTENSION postgis_topology;
        -- Enable PostGIS Advanced 3D
        -- and other geoprocessing algorithms
        -- for some reason the other CREATE EXTENSION commands don't work, but I don't seem to need them?
 gisdb> -- make sure to create a schema in the database into which you
        -- will load the raster:
 gisdb> CREATE SCHEMA gisdb

3. The GeoTIFF is a raster which contains all of the info I need. Convert this to a .sql file using raster2sql:

$ raster2pgsql -I -C -s 4326 GeoDB.TIFF gisdb.NASA > nasa.sql

This calls the raster2pgsql command (a bash script located in the /Applications/Postgres.app/Contents/Versions/9.4/bin folder).
http://gis.stackexchange.com/questions/62026/how-to-import-geotiff-via-postgis-into-geoserver

    -I: flag to create the spatial GiST index for performance
    -C: flag to apply the raster constraints
    -s 4326: SRID of NASA tiffs reported by tool gdalinfo. SRID is the code for the particular convention used to map coordinates to positions on the earth. Turns out to be WGS8 format which has SRID of 4326.
    GeoDB.tif: the TIFF in question
    gisdb.NASA: save into a new NASA table in the gisdb schema. By default this command will delete an existing copy of this table and create a new one of the same name
    >nasa.sql: make a nasa.sql file in the current working directory

$ psql -d gisdb -f nasa.sql

    This means something like open a pgsql repl with the database gisdb loaded, and load in the file nasa.sql.

BATCH LOADING


4. Query the database

gisdb> select st_nearestvalue(rast, ST_GEOMFromtext('POINT(13 26)',4326)) from gisdb.nasa;

select nearest value to a particular data point. NB: the rater may interpret 0s as empty values. There is a way to get around this:
gisdb> select st_nearestvalue(rast, ST_GEOMFromtext('POINT(-73.94 40.7127)',4326), false) from gisdb.nasa;

I think there's also a way to convert all of the 'nulls' at once
[official postgis docs for using raster data](http://postgis.net/docs/manual-2.2/using_raster_dataman.html)

[blog guide to quickstart make postgis db](http://live.osgeo.org/en/quickstart/postgis_quickstart.html#creating-a-spatial-table-the-easy-way)

[ST_nearest value docs](http://postgis.net/docs/manual-2.1/RT_ST_NearestValue.html)




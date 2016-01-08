
##Make the database and enable postgis functionality
makedb nasa

pgcli nasa

CREATE SCHEMA rainfall;

CREATE EXTENSION postgis;

CREATE EXTENSION postgis_topology;

##Converting all the files into the sql rasters
http://postgis.net/docs/manual-2.2/using_raster_dataman.html

raster2pgsql -c -C -s 4326 -n forecast_date *.tiff rainfall.rasters > rainfall_all.sql

-c                  --Create new table and populate it with raster(s), this is the default mode.
-C                  --Apply raster constraints -- srid, pixelsize etc. to ensure raster is properly registered in raster_columns view.
-s 4326             --Assign output raster with specified SRID. NASA rainfall data is WGS8
-n forecast_date    --Assign the forecast date to a new column called 'forecast_date'

psql -d nasa -f rainfall_all.sql

##Querying the database


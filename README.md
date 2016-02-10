# GeoDB
An API to query historical rainfall data. See the web app [here](http://rainfall-data.com:5000/) (a work in progress).

# Background
This app provides API access to historical [Tropical Rainfall Monitoring Mission (TRMM)](href = 'http://pmm.nasa.gov/trmm') precipitation data. The TRMM was a joint mission between NASA and the Japan Aerospace Exploration (JAXA) Agency to study rainfall for weather and climate research. The TRMM ran from Nov 1997 to April 2015, collecting over 17 years of daily rainfall data. This database was populated with daily rainfall measurements in floating point Geotiff format at 0.25° resolution, from the [NASA Earth Observations](href='http://neo.sci.gsfc.nasa.gov/view.php?datasetId=TRMM_3B43D') (NEO) site.

# Usage
Any global location within -50° and 50° latitude, and -180° and -180° can be queried, between 1 Jan 1998 and 30 Sept 2015. Data will be returned for the nearest point to the one queried. Please note: these data have been scaled and resampled for visualisation purposes by NEO, and are not suitable for rigorous scientific investigations. For more information, see [here](href=http://neo.sci.gsfc.nasa.gov/blog/2013/12/23/csv-and-floating-point-geotiffs/).

# API
API access to the database is also available; simply enter an URL of the form:

```
/api/rain_dump?start_date=yyyy-mm-dd&end_date=yyyy-mm-dd&latitude=latitude&longitude=longitude
```

You will be returned a JSON file. For example, the following returns the data for Manhattan between 1 Jan 1998 and 5 March 1999:

```
/api/rain_dump?start_date=1998-01-01&end_date=1999-03-05&latitude=40&longitude=-73
```

If you enter a location outside of the bounds of the dataset, you will be returned either -3.40282346638529e+38 or 99999.0, which are null values, or an empty JSON.

# Software stack
- Data scraped from [NASA NEO](http://neo.sci.gsfc.nasa.gov/view.php?datasetId=TRMM_3B43D&date=2015-09-01), using [Selenium](http://www.seleniumhq.org/).
- Data were then housed in a PostgreSQL with the [PostGIS extension](http://postgis.net/) enabled for location-based queries.
- The web app was made in [Flask](http://flask.pocoo.org/)


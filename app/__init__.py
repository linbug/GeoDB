from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import json
import psycopg2.extensions

app = Flask(__name__)
app.secret_key = 'some_secret'
conn = psycopg2.connect(dbname = 'nasatiled', user = 'flask', password = 'Om16uUlzZjxI').cursor()
cur = conn.cursor()

def return_json(start_date, end_date, latitude, longitude):
    # TODO: this query fixes a bug where we select invalid data by excluding the bounding boxes of areas
    # with no data.

    # select forecast_date from rainfall.rasters where forecast_date >= '1999-11-17' and
    # forecast_date <= '1999-12-24' and
    # st_intersects(rast, ST_GEOMFromtext('Point(0 0)',4326)) and
    # not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 50)'),st_geomfromtext('Point(180 90)'))) and
    # not st_intersects(rast, ST_makebox2D(st_geomfromtext('Point(-180 -90)'),st_geomfromtext('Point(180 -50)'))) order by forecast_date;

    cur.execute("""SELECT forecast_date, ST_nearestvalue(rast,ST_geomfromtext('Point(%s %s)',4326)) FROM rainfall.rasters \
                WHERE forecast_date >= %s \
                AND forecast_date <= %s
                AND ST_intersects(rast, ST_geomfromtext('Point(%s %s)',4326));"""
           , (float(longitude), float(latitude), start_date, end_date,float(longitude), float(latitude) ))
    rows = cur.fetchall()
    json_dict = {}
    for row in rows:
        json_dict[row[0][:-5]] = round(row[1],3)
    return json_dict

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def query():
    if request.method == 'POST':
        try:
            latitude = float(request.form["latitude"])
            longitude = float(request.form["longitude"])
            start_date = request.form["start_date"]
            end_date = request.form["end_date"]
            json_dict = return_json(start_date, end_date, latitude, longitude)
        except ValueError:
            return redirect(url_for('index'))
        if not (end_date or start_date):
            flash("Please select both start and end dates.")
        elif end_date<start_date:
            flash("Please ensure that end date is after start date.")
        else:
            return render_template('result.html', start_date = start_date, end_date = end_date, latitude = latitude, longitude = longitude, json_dict = json.dumps(json_dict, sort_keys=True))
    return redirect(url_for('index')) #redirects to index if GET request

# @app.route('/api/start_date=<start_date>&end_date=<end_date>&latitude=<latitude>&longitude=<longitude>')
#def return_json_page(start_date, end_date, latitude, longitude):
#    json_dict = return_json(start_date, end_date, latitude, longitude)
#    return json.dumps(json_dict, sort_keys=True)
@app.route('/api/rain_dump')
def return_json_page():
    start_date = request.args.get('start_date', '')
    end_date   = request.args.get('end_date', '')
    latitude   = request.args.get('latitude', '')
    longitude  = request.args.get('longitude', '')

    if len(start_date) == 0:
        return "Nope"

    json_dict  = return_json(start_date, end_date, latitude, longitude)
    return json.dumps(json_dict, sort_keys=True)
    # return 'Start date = {} \n End date = {} \n Location = {}'.format(start_date, end_date, latitude)

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    return "Oops! Page not found"

if __name__ == '__main__':
    app.run(debug=True)


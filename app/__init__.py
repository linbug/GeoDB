from flask import Flask
import psycopg2
import json

app = Flask(__name__)
conn = psycopg2.connect("dbname = 'nasa'")
cur = conn.cursor()

@app.route('/')
def hello_world():
    return 'NASA rainfall data'

@app.route('/start_date=<start_date>&end_date=<end_date>&latitude=<latitude>&longitude=<longitude>')
def return_json(start_date, end_date, latitude, longitude):
    cur.execute("""SELECT forecast_date, ST_nearestvalue(rast,ST_geomfromtext('Point(%s %s)',4326)) FROM rainfall.rasters \
                    WHERE forecast_date >= %s \
                    AND forecast_date <= %s;""", (float(longitude), float(latitude), start_date, end_date))
    rows = cur.fetchall()
    json_dict = {}
    for row in rows:
        json_dict[row[0][:-5]] = row[1]
    return json.dumps(json_dict, sort_keys=True)
    return 'Start date = {} \n End date = {} \n Location = {}'.format(start_date, end_date, latitude)

@app.errorhandler(404)
def not_found(error):
    return "Page not found"

if __name__ == '__main__':
    app.run(debug=True)


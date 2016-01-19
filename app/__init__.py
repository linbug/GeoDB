from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import json
import psycopg2.extensions

app = Flask(__name__)
conn = psycopg2.connect("dbname = 'nasaJan18'")
cur = conn.cursor()

def return_json(start_date, end_date, latitude, longitude):
    cur.execute("""SELECT forecast_date, ST_nearestvalue(rast,ST_geomfromtext('Point(%s %s)',4326)) FROM rainfall.rasters \
                WHERE forecast_date >= %s \
                AND forecast_date <= %s;""", (float(longitude), float(latitude), start_date, end_date))
    rows = cur.fetchall()
    json_dict = {}
    for row in rows:
        json_dict[row[0][:-5]] = (row[1])
    return json_dict

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
# @app.route('/new_query', methods = ['POST'])
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
        return render_template('result.html', start_date = start_date, end_date = end_date, latitude = latitude, longitude = longitude, json_dict = json_dict)
        # return 'Start date = {} \n End date = {} \n Location = {}'.format(start_date, end_date, latitude)
    return redirect(url_for('index')) #redirects to index if GET request





    # return redirect(url_for('result'))

# @app.route('/result')
# def result():
#     if not json_dict:
#         return redirect(url_for('index'))

    # return render_template('result.html', latitude = latitude, longitude = longitude, json_dict = json_dict)

@app.route('/start_date=<start_date>&end_date=<end_date>&latitude=<latitude>&longitude=<longitude>')
def return_json_page(start_date, end_date, latitude, longitude):
    json_dict = return_json(start_date, end_date, latitude, longitude)
    return json.dumps(json_dict, sort_keys=True)
    return 'Start date = {} \n End date = {} \n Location = {}'.format(start_date, end_date, latitude)


@app.errorhandler(404)
def not_found(error):
    return "Page not found"

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, request, render_template
import numpy as np

import time

app = Flask(__name__)

FLAG = "FLAG{good_job!_hopefully_the_corrective_radius_is_fine}"
THRESHOLD = 40 # radius to which guess is ok
TIME_WINDOW = 3 # length of submission window (technically half cause it's +- TIME_WINDOW) (backend thingo to allow for request delays)
RATELIMIT = 10 # number of seconds until submission window opens


ANSWER_LAT, ANSWER_LNG = -33.917243, 151.226392

def dist(x, y, z, nx, ny, nz):
    return ((nx - x)**2 + (ny - y) ** 2 + (nz - z) ** 2) ** 0.5

def latlngtoxyz(lat, lng):
    lat = np.deg2rad(lat)
    lng = np.deg2rad(lng)
    R = 6371 # radius of the earth
    return (
        R * np.cos(lat) * np.cos(lng),
        R * np.cos(lat) * np.sin(lng),
        R *np.sin(lat)
    )


@app.route("/")
def index():
    return render_template("index.html", ratelimit=RATELIMIT, threshold=THRESHOLD)

@app.route("/submit", methods=["POST"])
def submit():
    current_time = time.time()
    window_start1 = current_time - current_time % RATELIMIT
    window_start2 = current_time + RATELIMIT - current_time % RATELIMIT
    if current_time > window_start1 + TIME_WINDOW and current_time + TIME_WINDOW < window_start2:
        return "Request took too long", 403
    request_json = request.get_json()
    x, y, z = latlngtoxyz(ANSWER_LAT, ANSWER_LNG)
    gx, gy, gz = latlngtoxyz(request_json["lat"], request_json["lng"])
    if dist(
        x, y, z, gx, gy, gz
    ) * 1000 < THRESHOLD:
        return FLAG
    else:
        return "Incorrect coordinates"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
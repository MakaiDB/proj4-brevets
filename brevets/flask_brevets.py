#only gets km and sends it to acp_times.py to calculate open and close times
#implement the other measure and send calculated times back to the front end

"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############

BREVET_DISTANCES = [200, 300, 400, 600, 1000]

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times for one control.
    Expects URL args: km (control distance), brevet_dist (km),
    and begin_time (ISO 8601 string for the brevet start).
    Returns JSON: {"result": {"open": ..., "close": ...}}
    or {"result": {"error": "..."}} on bad input.
    """
    km = request.args.get('km', type=float)
    brevet_dist = request.args.get('brevet_dist', type=int)
    begin_time = request.args.get('begin_time', type=str)
    app.logger.debug("km={}, brevet_dist={}, begin_time={}".format(
        km, brevet_dist, begin_time))

    if km is None or km < 0:
        return flask.jsonify(result={"error": "Enter a distance of 0 or more km"})
    if brevet_dist not in BREVET_DISTANCES:
        return flask.jsonify(result={"error": "Invalid brevet distance"})
    if km > brevet_dist * 1.2:
        return flask.jsonify(result={"error": "Control is more than 20% past the brevet distance"})
    try:
        arrow.get(begin_time)
    except Exception:
        return flask.jsonify(result={"error": "Invalid start time"})

    open_time = acp_times.open_time(km, brevet_dist, begin_time)
    close_time = acp_times.close_time(km, brevet_dist, begin_time)
    return flask.jsonify(result={"open": open_time, "close": close_time})


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

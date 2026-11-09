"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#

#straight from the ACP website, used to calculate open and close times
#(segment start km, segment end km, min speed km/h, max speed km/h)
TIME_KEY = [
    (0,    200,  15,     34),
    (200,  400,  15,     32),
    (400,  600,  15,     30),
    (600,  1000, 11.428, 28),
    (1000, 1300, 13.333, 26),
]

#extraneous dictionary to hold the final close times for each brevet distance
FINAL_CLOSE_HOURS = {200: 13.5, 300: 20, 400: 27, 600: 40, 1000: 75}

def _to_minutes(hours):
    # Nearest minute; exact .5 ties go to the even minute (Python's round())
    return round(hours * 60)

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
   Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
   """
   controle = min(control_dist_km, brevet_dist_km)
# Used a table to elimate the need for a lot of for and if statements.
   hours = 0
   for lo, hi, min_speed, max_speed in TIME_KEY:
        km_in_segment = max(0, min(controle, hi) - lo)
        hours += km_in_segment / max_speed

   start = arrow.get(brevet_start_time)
   return start.shift(minutes=+_to_minutes(hours)).isoformat()
   

    


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
   """
   Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
   Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
   """
   start = arrow.get(brevet_start_time)

   if control_dist_km >= brevet_dist_km:
        # Final control: fixed limit, regardless of how far past it is
        hours = FINAL_CLOSE_HOURS[brevet_dist_km]
   elif control_dist_km <= 60:
        # Covers the 0 km start control too (0/20 + 1 = 1 hour)
        hours = control_dist_km / 20 + 1
   else:
        hours = 0
        for lo, hi, min_speed, max_speed in TIME_KEY:
            km_in_segment = max(0, min(control_dist_km, hi) - lo)
            hours += km_in_segment / min_speed

   return start.shift(minutes=+_to_minutes(hours)).isoformat()

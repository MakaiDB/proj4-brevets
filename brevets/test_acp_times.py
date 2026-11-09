import arrow
from acp_times import open_time, close_time

START = "2026-11-01T00:00:00+00:00"


def at(hours, minutes=0):
    """Expected time: START plus hours and minutes, as an ISO string."""
    return arrow.get(START).shift(hours=hours, minutes=minutes).isoformat()


def test_single_segment():
    # 100 km in a 200 brevet: 100/34 h = 2h56, 100/15 h = 6h40
    assert open_time(100, 200, START) == at(2, 56)
    assert close_time(100, 200, START) == at(6, 40)


def test_crosses_segment_boundary():
    # 350 km: 200/34 + 150/32 = 10h34 open; 350/15 = 23h20 close.
    # Using one speed for the whole distance (350/32) would give 10h56.
    assert open_time(350, 400, START) == at(10, 34)
    assert close_time(350, 400, START) == at(23, 20)


def test_start_control():
    assert open_time(0, 200, START) == at(0)
    assert close_time(0, 200, START) == at(1)


def test_final_control_fixed_close():
    assert open_time(200, 200, START) == at(5, 53)
    assert close_time(200, 200, START) == at(13, 30)


def test_control_past_brevet_distance():
    # 205 km on a 200 brevet is treated as 200 km
    assert open_time(205, 200, START) == open_time(200, 200, START)
    assert close_time(205, 200, START) == close_time(200, 200, START)


def test_long_brevet_slow_min_speed():
    # 890 km on a 1000 brevet crosses the 600 km boundary
    assert open_time(890, 1000, START) == at(29, 9)
    assert close_time(890, 1000, START) == at(65, 23)
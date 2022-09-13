import pytest
from helper import discretize, distance
from datetime import datetime

def test_discretize_down():
    # Given
    dt = datetime(year=2022, month=9, day=12, hour=6, minute=18)
    timeframe = 15
    # When
    result = discretize(dt, timeframe)
    expected = datetime(year=2022, month=9, day=12, hour=6, minute=15)
    # Then
    assert expected == result

def test_discretize_up():
    # Given
    dt = datetime(year=2022, month=9, day=12, hour=6, minute=26)
    timeframe = 15
    # When
    result = discretize(dt, timeframe)
    expected = datetime(year=2022, month=9, day=12, hour=6, minute=30)
    # Then
    assert expected == result

def test_discretize_nothing():
    # Given
    dt = datetime(year=2022, month=9, day=12, hour=6, minute=26)
    timeframe = 0
    # When
    result = discretize(dt, timeframe)
    expected = datetime(year=2022, month=9, day=12, hour=6, minute=26)
    # Then
    assert expected == result

def test_distance():
    # Given
    longitude_x = -94.29
    latitude_x = 28.5782
    longitude_y = -94.10
    latitude_y = 28.10
    # When
    result = distance(latitude_x, longitude_x, latitude_y, longitude_y)
    # Then
    assert round(result) == 56176
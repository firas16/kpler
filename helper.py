from datetime import datetime
from datetime import timedelta
from geopy.distance import geodesic as GD

def discretize(dt: datetime, time_frame: int):
    """
    discretizes time into frames of length time_frame
    :param dt: datetime
    :param time_frame: discretizing parameter
    :return: discretized datetime
    """
    time_frame = time_frame % 60
    if(dt.minute == 0 or time_frame == 0):
        return dt
    i = 0
    while(time_frame * i <= dt.minute):
        i+=1
    if(time_frame * i - dt.minute > time_frame/2):
        i-=1
    return  dt + timedelta(minutes=time_frame*(i)-dt.minute)

def distance(latitude_x, longitude_x, latitude_y, longitude_y):
    return GD((latitude_x, longitude_x), (latitude_y, longitude_y)).m

def distance_score(distance, distance_threshold, mid_distance_coefficient, mid_distance_score):
    if(distance < distance_threshold):
        return 1
    elif(distance < mid_distance_coefficient * distance_threshold):
        return mid_distance_score
    else:
        return 0

def speed_score(mother_speed, baby_speed):
    max_sp = max(mother_speed , baby_speed)
    if(max_sp == 0):
        return 1
    return 1 - abs(mother_speed - baby_speed)/max_sp

def global_score(distance_score, speed_score, distance_weight, speed_weight):
    score = distance_score * distance_weight + speed_score * speed_weight
    return score
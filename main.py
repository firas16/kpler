import pandas as pd
from helper import discretize, distance, distance_score, speed_score, global_score
from itertools import combinations
import yaml

#read config
with open("conf.yaml", "r") as yamlfile:
    conf = yaml.load(yamlfile, Loader=yaml.FullLoader)

#read positions file
df = pd.read_csv("data/input/Galveston_2017_11_25-26.csv", header=0, sep=';')

#extract vessel ids
vessels = df.vessel_id.drop_duplicates().tolist()

# set search parameters
global_score_threshold = conf["global_score_threshold"]         # global score threshold above which we consider the possibility of an STS
time_frame = conf["time_frame"]                                 # time discretization parameter
distance_threshold = conf["distance_threshold"]                 # distance under which distance score takes 1
mid_distance_coefficient = conf["mid_distance_coefficient"]     # defines distance of average score
mid_distance_score = conf["mid_distance_score"]                 # mid distance score
distance_weight = conf["distance_weight"]                       # distance score weoght in global score
speed_weight = conf["speed_weight"]                             # speed score weight in global score

df['received_time_utc'] = pd.to_datetime(df['received_time_utc'])
df["received_time_utc_discretized"] = df.apply(lambda x: discretize(x.received_time_utc, 15), axis=1)

#begin STS search
i = 0
for (vessel_i, vessel_j) in combinations(vessels, 2):
    print(vessel_i, vessel_j)
    data_vessel_i = df.where(df.vessel_id == vessel_i)[["vessel_id",
                                                        "received_time_utc_discretized", "longitude", "latitude",
                                                        "speed", "heading"]].dropna(how="all")
    data_vessel_j = df.where(df.vessel_id == vessel_j)[["vessel_id",
                                                        "received_time_utc_discretized", "longitude", "latitude",
                                                        "speed", "heading"]].dropna(how="all")

    result = data_vessel_j.merge(data_vessel_i, how='inner', on=["received_time_utc_discretized"])
    if (len(result) > 0):
        #compute distance between vesseils
        result["distance"] = result\
            .apply(lambda x: distance(x.latitude_x, x.longitude_x, x.latitude_y, x.longitude_y),axis=1)
        #compute distance score
        result["distance_score"] = result\
            .apply(
            lambda x: distance_score(x.distance, distance_threshold, mid_distance_coefficient, mid_distance_score), axis=1)
        # compute speed score
        result["speed_score"] = result.apply(lambda x: speed_score(x.speed_x, x.speed_y), axis=1)

        #compute global score
        result["global_score"] = result\
            .apply(lambda x: global_score(x.distance_score, x.speed_score, distance_weight, speed_weight), axis=1)

        #filter scores based on threshold
        agg_func_math = {
            'global_score':
                ['max']
        }
        scores = result.where(result["global_score"] >= global_score_threshold).groupby(
            ["vessel_id_x", "vessel_id_y", "received_time_utc_discretized"]).agg(agg_func_math)

        # persist results
        if (i == 0):
            result.to_csv("./data/output/STS_possibility.csv", sep=";")
            scores.to_csv("./data/output/STS_scores.csv", sep=";")
        else:
            result.to_csv("./data/output/STS_possibility.csv", sep=";", mode='a', header=False)
            scores.to_csv("./data/output/STS_scores.csv", sep=";", mode='a', header=False)

    i += 1

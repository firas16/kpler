# The Problem of Ship-To-Ship Cargo Transfer

In this project, we try to find STS transfers based on ship positions and speed.
Algorithm: compute a score of STS for each couple of vessels based on ship positions and speed.
We discretize time in order to have regular snapshots. for each snapshot, we compute score of STS.

## Requirements
- Git 2.17.1 or later
- python 3.7 or later

see requirements.txt for detailed packages

## Local Installation

You need to clone project into your local machine using:  
`git clone https://github.com/firas16/kpler.git`

Create virtualenv and Install requirements.

The project contains two main scripts:
- main.py: use to extract possible STS based on input CSV file containing ship data.
- viz.py: use to visualize ship coordinates on the map

## Configuration

You can play with the algorithm settings by changing parameters in conf.yaml:

- global_score_threshold: global score threshold above which we consider the possibility of an STS
- time_frame: time discretization parameter
- distance_threshold: distance under which distance score takes 1
- mid_distance_coefficient: defines distance of average score
- mid_distance_score: mid distance score
- distance_weight: distance score weight in global score
- speed_weight: speed score weight in global score

## Possible Enhancements

- Use ship status to filter data before applying algorithm (For example status 7 engaged in fishing)
- Use ship status in STS score
- Improve distance score calculation: current function very simple constant piecewise
- Improve positionning accuracy based on speed, course and heading
- Improve global scoring function: should be based not only on snapshot but on multiple snapshots
- Ameliorate code decoupling and test coverage
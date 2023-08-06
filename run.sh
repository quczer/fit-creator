#!/bin/bash
python src/fit_creator/scripts.py download-all-workout-pages --verbose
python \
    src/fit_creator/main.py export-zwift-workouts-to-wkt \
    --html_path data/html/zwift/workout_plans \
    --out_wkt_dir data/workouts/wkt \
    --verbose
python \
    src/fit_creator/main.py \
    export-wkt-workouts-to-fit \
    --wkt_path data/workouts/wkt/Build_Me_Up \
    --out_fit_dir data/workouts/fit \
    --verbose
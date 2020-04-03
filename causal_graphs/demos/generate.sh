#!/bin/bash

# scene="../scenarios/fallingBall_success.py"

blender_path="/Applications/Blender.app/Contents/MacOS/Blender"

path="../scenarios/"

echo 'Which Scene?'

read scene

#creates simu.pkl and scene.egg files
printf './'$scene | python3.7 import_scenario.py $path$scene".py"

blendfile=$scene".blend"

touch $blendfile

printf $scene".egg" | $blender_path -b --python import.py --python ../blender/clean_up_scene.py --python ../blender/import_keyframes2.py --python ../blender/render.py -- $scene

# ./Contents/MacOS/Blender -b blendfile -P ../blender/render.py -- 0




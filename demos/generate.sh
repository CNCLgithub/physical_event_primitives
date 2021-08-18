#!/bin/bash

# scene="../scenarios/fallingBall_success.py"

blender_path="/Applications/Blender.app/Contents/MacOS/Blender"

path="../scenarios/"

echo 'Which Scene?'

read scene

echo 'GUI Mode? (0 or 1)'

read debug

#creates simu.pkl and scene.egg files
printf './'$scene | python3.8 import_scenario.py $path$scene".py"

blendfile=$scene".blend"

touch $blendfile

if [ $debug == "0" ]
then
	printf $scene".egg" | $blender_path -b --python import.py --python ../blender/clean_up_scene.py --python ../blender/import_keyframes2.py --python ../blender/render.py -- $scene
else
	printf $scene".egg" | $blender_path --python import.py --python ../blender/clean_up_scene.py --python ../blender/import_keyframes2.py -- $scene
fi






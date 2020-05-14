#!/bin/bash

# scene="../scenarios/fallingBall_success.py"

#blender_path="/Applications/Blender.app/Contents/MacOS/Blender"
blender_path=/blender/blender

path="scenarios/"

echo 'Which Scene?'

read scene

echo 'Debugging Mode? (0 or 1)'

read debug


# if [[ $scene == *"2Ball"* ]]; then
# 	moving="2b"
# elif [[ $scene == *"2Plank"* ]]; then
# 	moving="2p"
# elif [[ $scene == *"BallPlank"* ]]; then
# 	moving="bp"
# elif [[ $scene == *"Ball"* ]]; then
# 	moving="b"
# elif [[ $scene == *"Plank"* ]]; then
# 	moving="p"
# else
# 	moving="n"
# fi

# echo $moving

# echo "What objects are movable? (b, p, 2b, 2p, bp)"

# read movable

#creates simu.pkl and scene.egg files
printf './'$scene | python demos/import_scenario.py $path$scene".py"

blendfile=$scene".blend"

touch $blendfile

if [ $debug == "0" ]
then
	printf $scene".egg" | $blender_path -b --python demos/import.py --python blender/clean_up_scene.py --python blender/import_keyframes2.py --python blender/render.py -- $scene
else
	printf $scene".egg" | $blender_path --python demos/import.py --python blender/clean_up_scene.py --python blender/import_keyframes2.py -- $scene
fi






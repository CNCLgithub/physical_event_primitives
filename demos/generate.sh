#!/bin/bash

# scene="../scenarios/fallingBall_success.py"

#blender_path="/Applications/Blender.app/Contents/MacOS/Blender"
blender_path=/blender/blender

path="scenarios/"

echo 'Which Scene?'

read scene

echo 'What seed number do you want to use for Gen?'

read trace_number

echo 'Debugging Mode? (0 or 1)'

read debug

 # step 1 : create the scene priors file if this seed has never been used before
if [[ ! -f "gen_jsons/scene_trace_${scene}${trace_number}.json" ]] 
then
    echo 'Creating a random instance of:' $scene
      
    julia demos/create_scene_priors.jl $scene $trace_number
    
else
    echo 'JSON file already created for this seed number. Skipping the Gen step.'
fi

# step 2 : creates simu.pkl and scene.egg files
printf './'$scene | python demos/import_scenario.py $path$scene".py"

blendfile=$scene".blend"

touch $blendfile

# step 3 : clean up the scene and render in blender
if [ $debug == "0" ]
then
	printf $scene".egg" | $blender_path -b --python demos/import.py --python blender/clean_up_scene.py --python blender/import_keyframes2.py --python blender/render.py -- $scene
else
	printf $scene".egg" | $blender_path --python demos/import.py --python blender/clean_up_scene.py --python blender/import_keyframes2.py -- $scene
fi






#!/bin/bash

# scene="../scenarios/fallingBall_success.py"

blender_path="/Applications/Blender.app/Contents/MacOS/Blender"

path="../scenarios/"

scene=$1
debug=$2

if [ -z "$1" ]
then
	echo 'Which Scene?'
	read scene
fi

if [ -z "$2" ]
then	
	echo 'GUI Mode? (0 or 1)'
	read debug
fi


#creates simu.pkl and scene.egg files
printf './'$scene | python3.8 import_scenario.py $path$scene".py"

blendfile=$scene".blend"

touch $blendfile

if [ $debug == "0" ]
then
	printf $scene".egg" | $blender_path -b --python import.py --python ../blender/clean_up_scene.py --python ../blender/import_keyframes2.py --python ../blender/render.py -- $scene
	
	# Turn it into a video
	mkdir -p ../output/movies/
	output_vid=../output/movies/$scene.mp4
	
	# run ffmpeg
	ffmpeg -r 30 -f image2 -s 1920x1080 -i %04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p $output_vid
	
	# Move the intermediate files somewhere else 
	mkdir -p createFiles/$scene
	mv $scene.egg $scene.pkl $scene.bam $scene.blend createFiles/$v
	
	# remove the pngs
	rm *.png

else
	printf $scene".egg" | $blender_path --python import.py --python ../blender/clean_up_scene.py --python ../blender/import_keyframes2.py -- $scene
fi







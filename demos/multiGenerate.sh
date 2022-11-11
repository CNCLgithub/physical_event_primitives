#!/bin/bash

for j in collision_collision collision_containment collision_falling collision_occlusion collision_topple containment_collision containment_falling containment_occlusion falling_containment falling_occlusion occlusion_collision occlusion_containment occlusion_falling occlusion_occlusion

do

	for i in 208
	do

		printf "${j}\n0\n" | ./generate.sh

		cd /tmp

		ffmpeg -r 30 -f image2 -s 1920x1080 -i %04d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p $j$i".mp4"

		rm -f *.png

		mkdir -p createFiles/$j$i

		mv $j.egg $j.pkl $j.bam $j.blend createFiles/$j$i

		# rm $j.egg $j.pkl $j.bam $j.blend

	done
done

#!/bin/bash

echo $1 # echo the input video 
for j in {1..60} # cycle through possible probe locations, up to 60 
do
	echo ${j} # what probe number? 
	start=$(bc <<< "scale = 1; ${j}*2/10") # when is the probe? (occurs every 200 ms)
	echo $start
	end=`echo "${start} + 0.125" | bc -l` # end of the probe will occur after about 125 ms

	# cut the video into three parts (pre-probe, probe, post-probe), slowing the video by half during the probe 
	ffmpeg -i ${1}".mp4" -filter_complex "[0:v]trim=0:0${start},setpts=PTS-STARTPTS[v1];
      [0:v]trim=0${start}:0${end},setpts=2*(PTS-STARTPTS)[v2];
      [0:v]trim=0${end},setpts=PTS-STARTPTS[v3];
      [v1][v2][v3] concat=n=3:v=1" ${1}"_"${j}".mp4"
      
 done

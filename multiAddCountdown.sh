#!/bin/bash

for i in *.mp4
do
	ffmpeg -i ../GreyCountdown.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
	ffmpeg -i ${i} -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts
	ffmpeg -i "concat:intermediate1.ts|intermediate2.ts" -c copy output.ts
	ffmpeg -i output.ts -c:v libx264 -c:a aac final_${i}
	rm intermediate1.ts intermediate2.ts output.ts ${i}
done

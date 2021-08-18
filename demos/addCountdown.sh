
for j in 2 4 5
do
	ffmpeg -i GreyCountdown.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
	ffmpeg -i collision/collision$j.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts
	ffmpeg -i "concat:intermediate1.ts|intermediate2.ts" -c copy output.ts
	ffmpeg -i ouput.ts -c:v libx264 -c:a aac cd_collision$j.mp4
	mv cd_collision$j collision
	rm intermediate1.ts intermediate2.ts output.ts
done

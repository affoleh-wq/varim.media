#!/bin/bash
# ./make.sh data/<slug>.json  -> out/<slug>/varim_<slug>_tiktok.mp4 (музыка всегда out/sound.wav)
set -e; cd "$(dirname "$0")"; J=$1; S=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['slug'])" $J)
mkdir -p out; [ -f out/sound.wav ] || cp sound.wav out/sound.wav
rm -f out/$S/s?.mp4
(python3 film.py render $J s1 s3 s5 & python3 film.py render $J s2 s4 & wait)
cd out/$S; printf "file s1.mp4\nfile s2.mp4\nfile s3.mp4\nfile s4.mp4\nfile s5.mp4\n" > list.txt
ffmpeg -y -loglevel error -f concat -i list.txt -c copy silent.mp4
ffmpeg -y -loglevel error -i silent.mp4 -i ../sound.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart varim_${S}_tiktok.mp4
echo done out/$S/varim_${S}_tiktok.mp4

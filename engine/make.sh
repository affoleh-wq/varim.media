#!/bin/bash
# ./make.sh data/<slug>.json  -> out/<slug>/varim_<slug>_tiktok.mp4 (музыка всегда out/sound.wav)
set -e; cd "$(dirname "$0")"; J=$1; S=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['slug'])" $J)
M=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('music','sound.wav'))" $J)
SC=$(python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(' '.join(d.get('scenes') or ['s1','s2','s3','s4','s5']))" $J)
mkdir -p out/$S
rm -f out/$S/s?.mp4
A=$(echo $SC | tr " " "\n" | awk "NR%2==1" | xargs); B=$(echo $SC | tr " " "\n" | awk "NR%2==0" | xargs)
(python3 film.py render $J $A & python3 film.py render $J $B & wait)
cd out/$S; for x in $SC; do echo "file $x.mp4"; done > list.txt
ffmpeg -y -loglevel error -f concat -i list.txt -c copy silent.mp4
ffmpeg -y -loglevel error -i silent.mp4 -i ../../$M -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart varim_${S}_tiktok.mp4
echo done out/$S/varim_${S}_tiktok.mp4

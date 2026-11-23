#!/bin/bash
# Карусель → вертикальный ролик-слайдшоу для TikTok.
# ./slideshow.sh <папка со slide_N.jpg> <выход.mp4>   (1080x1920, 30 fps, ~1.9 с на слайд, музыка sound_verdict.wav)
set -e
S=$1; OUT=$2; D=1.9; X=0.35; H=$(cd "$(dirname "$0")" && pwd)
N=$(ls $S/slide_*.jpg | wc -l); inputs=""; f=""
for i in $(seq 1 $N); do inputs="$inputs -loop 1 -t $D -framerate 30 -i $S/slide_$i.jpg"; done
for i in $(seq 0 $((N-1))); do f="$f[$i:v]split[a$i][b$i];[a$i]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2,eq=brightness=-0.25[bg$i];[b$i]scale=1080:-1,zoompan=z='1+0.0009*on':d=1:s=1080x1350:fps=30[fg$i];[bg$i][fg$i]overlay=0:150,format=yuv420p,trim=duration=$D,setpts=PTS-STARTPTS[v$i];"; done
prev=v0; for i in $(seq 1 $((N-1))); do off=$(python3 -c "print(round(($D-$X)*$i,3))"); f="$f[$prev][v$i]xfade=transition=slideleft:duration=$X:offset=$off[x$i];"; prev=x$i; done
T=$(python3 -c "print(round(($D-$X)*($N-1)+$D,2))"); F=$(python3 -c "print(round($T-0.8,2))")
ffmpeg -y -loglevel error $inputs -stream_loop -1 -i $H/sound_verdict.wav -filter_complex "${f%;}" -map "[$prev]" -map $N:a -t $T -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -af "afade=t=out:st=$F:d=0.8" "${OUT%.mp4}.tmp.mp4"
mv "${OUT%.mp4}.tmp.mp4" "$OUT"; echo ok $OUT $T



ffmpeg -y \
    -i src/music/_generated/generated_sample.mp4 \
    -vn -acodec libmp3lame -q:a 4 \
    src/music/_generated/generated_sample.mp3

ffmpeg -y \
    -i src/music/_generated/generated_sample.mp4 \
    -vn -acodec libmp3lame -q:a 4 \
    -af "afade=t=in:ss=0:d=5,afade=t=out:st=10:d=5" \
     src/music/_generated/faded_generated_sample.mp3

aws s3 cp src/music/_generated/generated_sample.mp4 s3://aipif-2023/media/

aws s3 cp src/music/_generated/faded_generated_sample.mp3 s3://aipif-2023/media/


timidity -Ow -o - src/music/_sample/music.mid \
    | ffmpeg -i - -acodec libmp3lame -ab 128k src/music/_generated/music.mp3

aws s3 cp src/music/_generated/music.mp3 s3://aipif-2023/media/


# ffmpeg -y \
#     -i src/music/_generated/generated_sample.mp3 \
#     -af "afade=t=in:ss=0:d=5,afade=t=out:st=10:d=5" \
#      src/music/_generated/faded_generated_sample.mp3


sudo apt-get install abcmidi timidity

abc2midi input.abc -o output.mid

timidity -Ow -o - output.mid \
    | ffmpeg -i - -acodec libmp3lame -ab 128k output.mp3

( 
    set -o xtrace ;
    
    tts \
        --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
        --list_speaker_idxs \
        > /tmp/speaker.txt

    cat /tmp/speaker.txt | tr "'" "\n" | egrep "[A-Z]" \
        | while read sp ; do 
            tts \
            --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
            --speaker_idx "$sp" \
            --language_idx "en" \
            --out_path  "src/speech/_generated/$sp.wav" \
            --text "From that day on, he sang not to be the best, but to bring joy and harmony, always remembering the wisdom of his master.  But the damage was done. The village never quite returned to the way it was, and Timmy learned a bittersweet lesson that stayed with him forever." ;
        done
)
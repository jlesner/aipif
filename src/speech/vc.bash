read -r -d '' stext << EOF
Months passed, and the town of Spick-and-Span announced an invention fair. The best invention would win a golden trophy and a tour of the famous Inventors' Academy. Lila was thrilled and worked day and night on her latest creation, while Charlie kept playing his games and eating chocolates.
One evening, Lila visited Charlie again. "Charlie, the fair is tomorrow! Do you have anything to show?"

Charlie looked worried, "I haven't had time, Lila. Maybe I can come up with something quick."

Lila shook her head, "You can't invent something great overnight, Charlie. You need to put in the work every day."

Charlie sighed, "I know, but I just couldn't stop playing my games."
EOF

tts \
    --model_name tts_models/multilingual/multi-dataset/xtts_v2 \
    --language_idx "en" \
    --speaker_wav  "/mnt/c/Users/chris/Downloads/attenborough0010.wav" \
    --out_path "src/speech/_generated/vc.wav" \
    --text "$stext"
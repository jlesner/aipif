export PYTHONPATH=~/aipif/src

[[ -f .env ]] || echo "make sure you have .env with keys setup ; see .env.example"

( 
    . flask_venv/bin/activate ; 
    while true ; do 
        # flask run
        python3 ~/aipif/src/app.py
        sleep 10 
    done
)

export PYTHONPATH=~/aipif/src

[[ -f .env ]] || echo "make sure you have .env with keys setup ; see .env.example"

flask run

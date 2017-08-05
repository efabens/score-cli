A python 3 script that writes sports scores to standard output

there are two scripts so far:
- score-cli-soccer.py does soccer scores
- score-cli.py does mlb scores

The source only update every five or so minutes, haven't figured out the exact rate.

there is some ansi color hardcoding, it looks good in iterm2. in os x terminal it is kinda weird, 
and it hasn't been tested anywhere else.

outside package requirements specified in the requirements.txt file. use `pip install -r requirements.txt`
# fyle_be_coding_challenge
Fyle Backend engineering coding challenge.

Host Url: http://172.105.39.232:5000

Steps to execute:-
1) sudo chmod 755 run.sh

2) nohup ./run.sh &

This repo contain 3 files.
1) run.sh (**This file will execute python api_py.py by passing 3 variable $user, $password, $database**)

2) api_py.py (**This file is responsible for connecting with postgres database and fetch data on the basis of query.**)

3) bank_detail.sh (**This file have 2 curl command which will fetch data.**)

Requirements for api_py.py

1) Postgres library (psycopg2)

2) Flask (flask)

3) nohup to run the server in background

4) Postgres db

Table schema:-
ifsc | state | city | bank_id | branch | address | district

Total data in table =127857

**Note**:- I have hosted this project on linode because i am very new to heroku and tried there to create all the requirements but fails and it was wasting my time.

After evaluation or every thing done from your side, please revert me back ASAP because i have to close this linode server.

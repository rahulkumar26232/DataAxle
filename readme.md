Some important points :

1# There is no code for freeing the parking spot after that hours,
easily be done via cronjob


Please find below Api request body:

1# signup (phone number or email both can be used ,pass only that )

curl --location 'http://127.0.0.1:8000/signup/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"rahulkumar26232@gmail.com",
    "password":"rahul"
    

}'


2# Login Api => for signin , initially i was going for Token Authentication

curl --location 'http://127.0.0.1:8000/signin/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"rahulkumar26232@gmail.com",
    "password":"rahul"
    

}'


3#  Parking Spot locations:


curl --location 'http://127.0.0.1:8000/parking-spot/fetch/?latitude=1&longitude=1&radius=10' \
--header 'Authorization: Basic cmFodWw6cmFodWw='

4# for reserving parking spot:

curl --location 'http://127.0.0.1:8000/parking-spot/reserve/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic cmFodWw6cmFodWw=' \
--data '{
    "parking_spot_id":3,
    "hours":5
    

}'


5# User history of parking spots

curl --location 'http://127.0.0.1:8000/parking-spot/reserved/list/' \
--header 'Authorization: Basic cmFodWw6cmFodWw='
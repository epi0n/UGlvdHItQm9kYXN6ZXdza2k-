# UGlvdHItQm9kYXN6ZXdza2k= (sanic web app)
A basic asynchronous web server application allowing to perform CRUD
 operations on PostgreSQL db with the usage of REST Api. 

Technologies used:
- Python3.7 - programming language
- Sanic - web server/api
- SqlAlchemy - ORM
- Alembic - database migrations
- PostgreSQL - database engine
- Docker-compose - deployment 


### How do I run this stuff?

Start off with cloning this repo. 

Setting up the application is made easy and OS independent with the usage
 of docker-compose:
 1. Install docker & docker-compose
 2. Change your current directory to project root
 3. Run command: `docker-compose build`
 
To run the app in your current terminal, run command:
- `docker-compose up`

If you prefer to run it as a daemon (background mode), run command:
- `docker-compose up -d`

This application is hosted, by default, at localhost:8080 and in DEBUG mode.

If you wish to edit database user/password/name - make appropriate
changes in the `.env` file in the root directory of this repository. 


### What does this thing even do?

As mentioned in the first section of this highly sophisticated readme
file, this application allows you to perform some basic CRUD operations
on the PostgreSQL database which is being hosted in a docker container.

This application lets you provide to it URLs of websites. 

Along with the URL, you will provide a time interval.
 
Every `{interval}` seconds, this website will be queried, and the response returned will be saved
in the database.

### API Endpoints

A short description of the endpoints:

---

**POST** `localhost:8080/api/fetcher`

Example usage:

`curl -si 127.0.0.1:8080/api/fetcher -X POST -d '{"url": "https://httpbin.org/range/10","interval":5}'`

This method lets you upload a `URL` to a website that you wish to be queried,
along with the time `interval` in seconds.

---

**GET** `localhost:8080/api/fetcher`

Example usage:

`curl -si 127.0.0.1:8080/api/fetcher`, or just enter the URL in your 
browser.

This method will return all the `ID`s and `URL`s that were POSTed into
the database. 

---

**DELETE** `localhost:8080/api/fetcher/{id}`

Example usage:

`curl -s 127.0.0.1:8080/api/fetcher/1 -X DELETE`

This method will delete the URL with id equal to `{id}` from the database,
along with all the data that was ever fetched for this record. 
No data will be downloaded from this URL anymore.


---

**GET** `localhost:8080/api/fetcher/{id}/history`

Example usage:

`curl -s 127.0.0.1:8080/api/fetcher/1/history`

This method will return all the responses ever received from the URL
with the provided `{id}`, along with the download `duration` time in seconds,
 and a UNIX `created_at` timestamp.

---


### Database

Database data is persistent - the state will be saved between your docker
runs. If you wish to check the state of the database by yourself,
you can "ssh" into the docker & access the db in the following way:

1. `sudo docker -exec -it postgres_db /bin/bash`
2. `psql -U docker`

And that is all. You can query the database tables by yourself in real-time
to check how the records are changing over time.

Database connection pool has been limited to 100 connections. You can
modify this value in `app/database/connector.py` file.


### Are there any tests done?

No. But I could add them per request, if anybody would need it.


### Feedback

If you find my app lacking, or you see places for improvement (even I do
see some, but I am an enemy of premature optimization), please make sure
to contact me @ ***epion1334@gmail.com***.
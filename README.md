# kode_test_2024
Kode test task 2024 for backend Python developer.  

## Stack
- Python 3.11
- Flask
- SQLAlchemy
- PostgreSQL
- Docker
- Postman

## Installation
1) Clone repository.
2) Run the following command
```docker compose -f compose.yaml up --build```
3) As it finishes building, open a separate tab of the console and type
```
docker exec notes_api-flask-app-1 python cli.py recreate_db
```
```
docker exec notes_api-flask-app-1 python cli.py add_test_data
```
This will drop all tables in the database, recreate them and add users "test" and "test2". Passwords are the same as usernames.
After that you may access the API at 0.0.0.0:5200/api/hello

## Routes
- Hello testing route: /api/hello [GET]
- Get all your notes: /api/notes [GET]
- Get a specific note of yours: /api/notes/<int:note_id> [GET]
- Add a note: /api/notes/new [POST] - requires name:str, content:str as json
- Authorize at: /api/notes/authenticate [POST] - requires username:str, password:str


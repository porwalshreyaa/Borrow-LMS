# See Demo

[Video Demo](https://drive.google.com/file/d/1vu26B6KIASCwU2UtbbJq0XcWHbaep4lp/view?usp=sharing)

# To start

Setup virtual environment and run command `./lrun.sh`



# User APIs


## Get:

#### Read one
curl http://127.0.0.1:5000/api/user/user_id

#### Read All
curl http://127.0.0.1:5000/api/user

## Post:

#### Create
curl -X POST http://localhost:5000/api/user -H "Content-Type: application/json" -d '{"username": "My name", "password":"mypassword_shhh", "email": "myemail@gmail.com"}'

## Put:
 
#### Update
curl -X PUT http://localhost:5000/api/user/user_id -H "Content-Type: application/json" -d '{"username": "My name", "password":"mypassword_shhh", "email": "myemail@gmail.com"}'

## Delete:

curl -X DELETE http://localhost:5000/api/user/user_id


# Book APIs


## Get:

#### Read one
curl http://127.0.0.1:5000/api/book/book_id

#### Read All
curl http://127.0.0.1:5000/api/book

## Post:

#### Create
curl -X POST http://localhost:5000/api/book -H "Content-Type: application/json" -d '{"name": "My Markus Book", "content": "This is my booooooook.", "path": "book.pdf", "cover": "cover.jpg", "authors": "Author"}'

## Put:
 
#### Update
 curl -X PUT http://localhost:5000/api/book/book_id -H "Content-Type: application/json" -d '{"name": "New Book Name", "content": "content", "path": "path.pdf", "cover": "cover.jpg", "authors": "Author"}'

## Delete:

curl -X DELETE http://localhost:5000/api/book/book_id


# Section APIs


## Get:

#### Read one
curl http://127.0.0.1:5000/api/section/section_id

#### Read All
curl http://127.0.0.1:5000/api/section

## Post:

#### Create
curl -X POST http://localhost:5000/api/section -H "Content-Type: application/json" -d '{"name": "section", "description": "description", "dateCreated": "date"}'

## Put:
 
#### Update
curl -X PUT http://localhost:5000/api/section/section_id -H "Content-Type: application/json" -d '{"name": "new name", "description": "new description", "dateCreated": "new date"}'

## Delete:

curl -X DELETE http://localhost:5000/api/section/section_id


# Book Section Assign APIs


## Post:

#### Create
curl -X POST http://localhost:5000/api/book/book_id/section/section_id

## Delete:

ccurl -X DELETE http://localhost:5000/api/book/book_id/section/section_id

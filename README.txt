Project deployment:

Step 1:
Install Node.js and MongoDB.

Step 2:
Install Mongoose through "npm install mongoose --save", in the project directory.

Step 3:
Run "mongod" in one terminal and "npm start" in another, in the project directory.
----------------------------------------------------------

Run commands:

We ran all our commands through postman. Select “x-www-form-urlencoded” to specify body.

Get all: GET http://localhost:3000/tasks/

Get specific: GET http://localhost:3000/tasks/:short

Delete specific: DELETE http://localhost:3000/tasks/:short

Delete all: DELETE http://localhost:3000/tasks/

Add new: POST http://localhost:3000/tasks/
		body: name: url (required), short: short url (if not specified it will be automatically generated)

Update short name: PUT http://localhost:3000/tasks/:short
					body: short: new short url
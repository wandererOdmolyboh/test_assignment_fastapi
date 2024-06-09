# test_assignment_fastapi
Developed a service using FastAPI and PostgreSQL, which includes a basic role system, request handling and storage, and message sending to Telegram.  The service is designed to be scalable and maintainable, with clear separation of concerns and modular code.


This application follows endpoints for user management and authentication using FastAPI:
1. POST /user/users/: Creates a new user and assigns a role to them. The current user must be authenticated. The role assigned to the new user depends on the role of the current user.
2. POST /oauth2/login: Authenticates a user and generates an access token for them. The user must provide their username and password. If the username and password are correct, an access token is generated and returned.
3. POST /messages/message/: Creates a new message and sends it to a specified chat in Telegram. The current user must be authenticated. After the message is created, it is sent to the specified chat in Telegram.
4. GET /user/users/: Returns a list of all users. The current user must be authenticated.  
5. GET /user/users/{user_id}/: Returns the details of a specific user. The current user must be authenticated.  
6. GET /messages/messages/: Retrieves all messages based on the role of the current user. If the current user is an admin, all messages are returned. If the current user is a manager, only messages sent by this manager and users created by this manager are returned. If the current user is a user, only messages sent by this user are returned. The current user must be authenticated.


How to run the application:

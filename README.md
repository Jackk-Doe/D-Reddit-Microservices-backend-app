# D-Reddit Microservices backend app, with Custom APIGateway and OAuth2 account system
Blogging or story posting in rooms backend app in microservices architecture.

Similar to Reddit or Medium.

Also use this project for INFS605 Microservices assignment


## Tech stack used : 
* FastAPI 
* NodeJS 
* PostgreSQL 
* MongoDB


## Current avialable Apps and Services list
- Client API Gateway
  - Written in FastAPI. 
  - Use this as a gateway to connect to all other services.
  - Only the routes specify in this app that Client users are supposed to have requests to.
- Post-services
  - Written in FastAPI.
  - Only this service would have access to POST database (PostgreSQL)
  - This service handles  rooms (post or story) and messages (comment in rooms) READ, CREATE, UPDATE, DELETE
- User-services
  - Written in NodeJS.
  - Uses OAuth2 security protocol, Bearer token verification.
  - Only this service has access to USER database (MongoDB)
  - Handling users account related requests : SignUp, SignIn, Generate-Token, Verify-Token.
- Content-Recommend-Services
  - Written in FastAPI
  - Generate recommend topics ID and amount (in dict[int,int])
  - Recommending topics are based on User's history viewed topics (User.views)
  
  
## To Run App
- NOTE : Suggest using Docker to create container and run the project.
- NOTE : If running only single app or service. Run database first, if that service must be connect to a database.

### 1. Run all
Running **all the apps and services** via Docker-compose in root folder with these commands :
```
docker compose up
```


### 2. Run only one app or service
Suggest using these 3 ways to run only one service.<br />
Must go to app or service folder.

1. `docker compose up`, if the app or service contains **docker-compose.yml** file.
2. `python app/main.py`, if the app or service is FastAPI-based
3. `node index.js` or `nodemon index.js`, if the service is User-services (NodeJS-based)

- NOTE : Must run a database first if the service is **Post-services** or **User-services** or **Content-filter-services**
- NOTE : If running services via `python xxx` or `node xxx` commands, .env file must be set up (see example in .env.example or Dockerfile)


## Test the application
Since the custom API Gateway app is written in FastAPI, it comes with built-in OpenAPI documentation page, generate by Swagger,<br />
which contains all informations about the routes of available in API Gateway.<br />

open : ```http://localhost:3000/docs```

![Screen Shot 2022-09-29 at 6 19 58 PM](https://user-images.githubusercontent.com/74220155/192945280-192e79c9-ce48-4240-8d48-6656e9ab9739.png)


Alternatively, test the app directly with a tool like Postman or similar tools.<br />

NOTE : 3000 is the default PORT value of the Gateway, change in Dockerfile or .env<br /><br />

## High level Backend Microservice System design
Expectation design of the final product :

![microservices backend design](https://user-images.githubusercontent.com/74220155/187069379-d5922ceb-63bf-4c41-93a7-390221cafa1b.jpg)


## TODO list:
TODO list, to complete this project (probably)
- [ ] Finish Backend Microservices
  - [X] APIGateway
  - [ ] Admin APIGateway (Access to all routes)
  - [X] Post-services
  - [X] User-services
  - [X] Content-recommend-services
  - [ ] Content-filter-services
  - [ ] Admin-services (ADMIN USE)
  - [X] POST database
  - [X] USER database
  - [ ] FILTER KEYS database
  - [X] Dockerise app
  - [ ] Use kubernetes to organise all containers
  - [ ] Upload to some serverless cloud provider
- [ ] Mobile Frontend app (Flutter)
  - [ ] Access to Backend API
  - [ ] Upload to PlayStore
  - [ ] Upload to AppStore
- [ ] Admin control app (Python Typer)
  - [ ] Access to Backend API

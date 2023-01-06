<p align="center">
<img src="https://i.ibb.co/C7Nm7Qb/ieloro-mini-logo.png" alt="ieloro-mini-logo" border="0">
</p>

# ielo backend

<i>=> Backend api microservices for the social commerce application **ielo**
</i>

## Brief

The **ielo backend** repository consists of an 10-tier microservices apis all working together to build a web-base marketplace where users can sell/buy/rent listings in different categories such as job posts, goods etc.

## Screenshots

_TBA_

## Quickstart

1. **Clone this repository.**

```
git clone https://github.com/Ielo-ro/backend.git
cd backend
```

2. **Build Docker images and run services**

```
docker-compose up
```

## Database Schemas

<a href="https://ibb.co/zhRQ1Mq"><img src="https://i.ibb.co/kg85p7N/ieloro-schemas.png" alt="ieloro-schemas" border="0"></a>
<br>
<i>THIS IS NOT THE FINAL SCHEMA AND IS SUBJECT TO CHANGE IN THE COMING DAYS </i>

Each microservice has its own MongoDB database and can only be accessed through their respective endpoints

## Architecture

**ielo** is composed of 10 microservices written in python programming
languages that talk to each other over HTTP & WebSockets.

[architecture_diagram_here]

| Service                              | Specific Tech                       | Description                                                             |
| ------------------------------------ | ----------------------------------- | ----------------------------------------------------------------------- |
| [gateway](./src/gateway_service)     | JWT                                 | Handles Authentication and offers Authorization for protected services. |
| [listing](./src/listing_service)     | PyMongo                             | Core service                                                            |
| [users](./src/)                      | Pymongo, JWT                        | Offers endpoint for user creation etc                                   |
| [messenger](./src/messenger_service) | Pymongo, Redis, FastAPI Web Sockets | Handles realtime chat                                                   |
| [email](./src/email_service)         | SendGrid                            | Offers endpoints for sending email verification etc                     |

<i>Few more services coming up</i>

This documentation is still underdevelopment

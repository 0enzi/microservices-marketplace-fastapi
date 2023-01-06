# Email Microservice

## Brief

**1. This microservice uses SendGrid, a cloud-based email service provider, to send and receive emails. It is configured with the SendGrid API key and sends emails using FastAPI SMTP relay.**

**2. The microservice exposes a set of RESTful APIs that allow the other services to send emails by making HTTP requests to the microservice. It provides APIs for email address validation and verification, allowing users to confirm that their email addresses are valid and properly formatted.**
_This will be displayed in the frontend_

**3. The microservice includes support for email templating and rendering, allowing users to customize the appearance and layout of their emails using HTML and CSS. It also provides support for internationalization, allowing emails to be localized and translated into different languages.**

**4. In addition to sending and receiving emails and as the application grows and scales outside MVP the microservice will provides tools for managing and organizing email lists, as well as tracking email delivery and engagement metrics. It will also be used to send newsletters, marketing emails, and other types of bulk emails to large groups of recipients.**

## Tech Stack

| Core Libraries         | Database |
| ---------------------- | :------: |
| SendGrid, FastAPI-MAIL |  Redis   |

## Screenshot

#### Email Verification

<img src="https://i.ibb.co/k4CW0Gj/emai-verification.png" alt="email-verification" border="0">

## Flow

#### Email Verification

1.  The user signs up for the service and provides their email address.
2.  The server generates a unique verification token using the `generate_verification_token` function.
3.  The server stores the token in the Redis database with an expiration time of one hour.
4.  The server sends an email to the user's email address with a link that includes the verification token.
5.  The user clicks the link in the email to verify their account.
6.  The server receives the request with the token and retrieves the token from the Redis database.
7.  If the token is found in the database and has not expired, the server marks the user's account as verified.
8.  If the token is not found in the database or has expired, the server returns an error message.

This process ensures that the verification tokens are unique and can only be used once within a certain time frame, which helps to prevent abuse and ensure the security of the verification process.

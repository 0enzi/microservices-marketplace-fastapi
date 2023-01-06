# Users Microservice

**This microservice is handles user creation, management and is used by gateway service to authorize as well as Admin for user related operations.**

## Tech Stack

| Core Libraries              | Database |
| --------------------------- | :------: |
| PyMongo, Pydantic, Odmantic | MongoDB  |

## Screenshot

<img src="https://i.ibb.co/DWMYtwG/doc-screenshot.png" alt="doc-screenshot" border="0"/>

## Models

#### UserInDB Class

The `UserInDB` class is a data model that represents a user in a database. It has the following fields:

- `account_info`: a dictionary containing additional information about the user's account and is used in custom roles. If a user picked individual role, it will contain `full_name`. If the user picked business type it will contain `business_name`, `busines_url`, `business_type`
- `username`: the user's username.
- `email`: the user's email address.
- `hashed_password`: the user's hashed password.
- `phone`: the user's phone number.
- `location`: the user's location.
- `created_at`: the date and time when the user's account was created.
- `account_type_id`: the ID of the user's account type.
- `is_super_admin`: a boolean value indicating whether the user is a super administrator.
- `status`: a boolean value indicating the user's account status.
- `email_verified`: a boolean value indicating whether the user's email address has been verified.
- `phone_verified`: a boolean value indicating whether the user's phone number has been verified.

The `Config` inner class specifies that the `users` collection should be used to store documents representing `UserInDB` instances.

#### UserInDB Class

The `AccountType` class is a data model that represents an account type in a database. It has the following fields:

- `account_type_name`: the name of the account type.
- `permissions`: a list of permissions associated with the account type.
- `open_for_registration`: a boolean value indicating whether the account type is open for registration.
- `status`: a boolean value indicating the status of the account type.

The `Config` inner class specifies that the `accountTypes` collection should be used to store documents representing `AccountType` instances.

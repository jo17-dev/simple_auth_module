# SAM – Simple Authentication Module

SAM is an open source project that provides a simple and reusable authentication module. It allows you to manage users and authenticate them using tokens, following an approach similar to services like Firebase, while remaining self-hosted and easy to integrate into existing projects.

The project is written in Python using **FastAPI** and exposes a REST API dedicated to authentication and user management based only on thiers emails, password and role


## Main Features

- User management (create, update, delete)
- Token-based authentication
- REST API built with FastAPI
- Containerized using Docker
- Ready-to-use setup with `Dockerfile` and `docker-compose`
- Unit tests (work in progress)

## Installation and Usage

The project includes:
- a `Dockerfile` to build the image
- a `docker-compose.yml` to quickly start all required services

This setup allows SAM to be launched easily, without complex configuration, both for development and local testing environments.

## Vision and Future Work

Planned improvements for SAM include:

- Implementing a admin management for roles and other users
- Completing and improving unit test coverage
- Role and permission management handled by an administrator
- Internationalization of strings to support multiple languages

## Contributing

SAM is an open source project and contributions are welcome.  
You can submit improvements, bug fixes, or new features through pull requests.

Feel free to [contact me](https://www.linkedin.com/in/joel-t-0745a4283/) if you would like to discuss the project or propose future enhancements.


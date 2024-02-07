# ToDo Application

## Overview

This ToDo Application serves as a test task, developed over the course of 4 hours to showcase the creation of a web-based ToDo list manager using Django and Django REST Framework (DRF). Fully containerized with Docker for ease of deployment and featuring a Makefile for simplified command execution, this project demonstrates essential functionalities including user authentication, task management, and automated reminders via a Celery-beat.

## Features

- **JWT User Authentication:** Secure login and registration functionality. Utilize JWT tokens for access and refresh mechanisms to ensure secure API calls.
- **Task Management:** Add, update, delete, and view tasks with ease.
- **Task Filtering:** Filter tasks based on category (work, private, learning) or completion status.
- **Automated Task Reminders:** A Celery beat task periodically checks for due tasks and notifies users accordingly.

## Getting Started

### Prerequisites

- Docker
- Docker-compose
- make

### Environment Setup

Create a `.env` file in the root directory of the project and populate it with the necessary environment variables as per the `.env.example` file.

### Running the Application

To run the application in demo mode, execute the following command:

`make demo`

This command will build all necessary Docker containers, create database roles (based on the `.env` file), and create 5 test users (`test_user0` to `test_user4`) with the password `test` and test data.

### Creating a Custom User

To create a custom user, you can use the following command:

`make django_manage cmd="createsuperuser"`

Follow the prompts to complete the creation of a new superuser.

## API Endpoints

- **Auth:** `api/auth/` authentication endpoints
- **Token create:** `api/auth/token/` for creating JWT access and refresh tokens. Access token lasts for 5 minutes and is required for all requests except `api/auth`. Use `api/auth/token/refresh` to refresh your access token.
- **Token:** `api/auth/token/` for refreshing JWT access token.

- **ToDO:** `api/todo/` To Do endpoints
- **ToDo List and Creation:** `api/todo/` GET/POST to retrieve a list of tasks, with filtering options for category (`work`, `private`, `learning`) and completion status. Accepts `description`, `category`, `due_date`, fields in **body** POST request.
- **ToDo CRUD:** `api/todo/<id>/` GET, PATCH, PUT, DELETE for managing a specific task. Accepts `description`, `category`, `due_date`, and `is_completed` fields in **body** PATCH, PUT request.

## Postman Collection

A Postman collection and environment file with all endpoints and scripts are available in the `data` folder for easy testing and demonstration of API functionalities.

## Celery Beat Task

A Celery beat task is included to periodically check the due dates of tasks and send notifications to users if the due date is approaching or has arrived.

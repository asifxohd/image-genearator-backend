# OpenAI DALL·E 2 Powered Image Generation Backend

Welcome to the backend repository for our image generation service powered by OpenAI's DALL·E 2 model. This backend is built using Python Django REST Framework and integrates various functionalities including image generation from prompts, user profile management, admin user management, and JWT authentication.

## Features

- **OpenAI DALL·E 2 Integration**: Utilizes OpenAI's DALL·E 2 model for generating images from prompts.
- **User Profile Management**: Allows users to create and manage their profiles.
- **Admin User Management**: Provides admin users with control over user accounts and permissions.
- **JWT Authentication**: Implements JWT (JSON Web Token) authentication for secure access to endpoints.

## Setup Instructions

1. Clone the repository:
   - https://github.com/asifxohd/image-genearator-backend.git
2. Install dependencies:
   - pip install -r requirements.txt
3. Configure environment variables:
   - Set up environment variables for DALL·E 2 API keys, database settings, and JWT secret key.
4. Run migrations:
  - python manage.py migrate
5. Run the development server:
  -python manage.py runserver
6. Access the API endpoints at `http://localhost:8000/api/`.

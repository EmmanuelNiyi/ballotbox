# Readme

# BallotBox Application

## Overview

BallotBox is a comprehensive web application designed to streamline the election process. It allows users to participate in elections, view results, and manage election activities. The platform ensures secure and efficient handling of elections, from registration to the final tally of votes.

## Features

- **User Registration and Activation**: Users can register and activate their accounts via email verification.
- **Login and Dashboard**: Authenticated users can access their personalized dashboard displaying available elections.
- **Election Search**: Users can search for elections using a unique election ID.
- **Election Registration**: Users can register for elections they are interested in.
- **Election Management**: Managers can create elections and add users to them.
- **Result Viewing**: Users can view the results of elections they have participated in.

## Roles and Permissions

- **Admins**: Have full access to all features and management capabilities within the application.
- **Election Managers**: Responsible for creating and managing elections but do not have admin privileges.

## Installation

### Prerequisites

- Python 3.x
- Django
- PostgreSQL (or any other preferred database)

### Steps

1. **Clone the repository**:
    
    ```
    git clone <https://github.com/EmmanuelNiyi/BallotBox.git>
    cd BallotBox
    
    ```
    
2. **Create a virtual environment**:
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`
    
    ```
    
3. **Install the dependencies**:
    
    ```
    pip install -r requirements.txt
    
    ```
    
4. **Configure the database**:
    - Update the `DATABASES` setting in `BallotBox/settings.py` to reflect your database configuration.
5. **Apply migrations**:
    
    ```
    python manage.py makemigrations
    python manage.py migrate
    
    ```
    
6. **Create a superuser**:
    
    ```
    python manage.py createsuperuser
    
    ```
    
7. **Run the server**:
    
    ```
    python manage.py runserver
    
    ```
    

## Usage

### Registration and Activation

1. Navigate to the registration page.
2. Fill out the registration form.
3. Check your email for the activation code.
4. Enter the activation code on the provided page to activate your account.
5. After activation, log in using your credentials.

### Participating in Elections

1. After logging in, navigate to your dashboard.
2. Use the search functionality to find elections using the election ID.
3. Register for elections you are interested in.
4. Participate in the elections and cast your vote.

### Managing Elections

1. Log in as an election manager.
2. Navigate to the election management section.
3. Create new elections and add users to these elections.

### Viewing Results

1. Navigate to the results page.
2. View the results of the elections you have participated in.

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](https://www.notion.so/LICENSE) file for details.

## Contact

For any inquiries or support, please contact:

- **Name**: Emmanuel Niyi-Oriolowo
- **Email**: [emmanuelniyioriolowo@gmail.com](mailto:emmanuelniyioriolowo@gmail.com)
- **Phone**: 08162556471

## Links

- [GitHub Repository](https://github.com/EmmanuelNiyi/BallotBox)

Thank you for using BallotBox!

## Environment Variables

Create a `.env` file in the root directory of your project and add the following configuration:

```
# Django settings
DEBUG=True
ALLOWED_HOSTS='localhost,127.0.0.1'
SECRET_KEY='your-secret-key'

# Database settings
DATABASE_NAME='your-database-name'
DATABASE_USER='your-database-user'
DATABASE_PASSWORD='your-database-password'
DATABASE_HOST='your-database-host'
DATABASE_PORT='your-database-port'

# Email settings
EMAIL_HOST='your-email-host'
EMAIL_HOST_USER='your-email-user'
EMAIL_HOST_PASSWORD='your-email-password'
EMAIL_PORT='your-email-port'
```
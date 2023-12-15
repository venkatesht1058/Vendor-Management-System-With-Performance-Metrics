# Vendor-Management-System-With-Performance-Metrics
This Django-based Vendor Management System allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics. Follow the instructions below to set up the system and explore the API endpoints.
## Setup Instructions
### 1. Clone the repository:
 - gh repo clone venkatesht1058/Vendor-Management-System-With-Performance-Metrics
 - cd vendor-management-system*
### 2. Create a virtual environment:
- python -m venv venv
### 3. Activate the virtual environment:
#### On Windows:
- .\venv\Scripts\activate
#### On macOS/Linux:
- source venv/bin/activate
### 4. Install dependencies:
- pip install -r requirements.txt
### 5. Apply migrations:
- python manage.py makemigrations
- python manage.py migrate
### 6. Run the development server:
- python manage.py runserver
### 7. Access the API at http://127.0.0.1:8000/api/
## Test Suite Instructions
### Running Tests
#### To run the test suite, use the following command:
- python manage.py test










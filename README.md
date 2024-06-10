# event-management
Develop a RESTful API service that manages events.

Cloning the repository
--> Clone the repository using the command below :

git clone https://github.com/naveenprakashjk24/event-management.git
--> Move into the directory where we have the project files :

cd eventManager
--> Create a virtual environment :

# Let's install virtualenv first
pip install virtualenv

# Then we create our virtual environment
virtualenv venv
--> Activate the virtual environment :

venv\scripts\activate
--> Install the requirements :

pip install -r requirements.txt
Running the App
--> To run the App, we use :

uvicorn main:app --reload
⚠ Then, the development server will be started at http://127.0.0.1:8000/

refer the swagger document for API list

http://127.0.0.1:8000/docs

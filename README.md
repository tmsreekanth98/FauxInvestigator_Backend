# FauxInvestigator_Backend
The backend REST API based server to handle incoming requests from the client and give prediction results. Uses Django, Django REST Framework, SQLite DB.

# Installation Instructions

1) Clone this repository
2) Run pip install -r requirements.txt
3) Run python manage.py migrate
4) Run python manage.py runserver


#Run using Docker Image

1) Install Docker
2) Run the following commands in order

      > docker pull tmsreekanth98/fauxinvestigator_server:1.02
      > docker run -p 8000:8000 -it tmsreekanth98/fauxinvestigator_server:1.02 sh
         # python manage.py runserver 0.0.0.0:8000
         
3) In the above commands replace 1.02 by the latest tag in the Docker Hub repository

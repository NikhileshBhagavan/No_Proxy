# Attendance Management System
Facial Recognition Based Attendance System using python,django,postgresql database and pg-admin for campanies, school and colleges, etc. 

![image](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) 
![image](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![image](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![image](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E) 

## Getting Started
### Prerequisites

Make sure you have installed *visual studio c++*, *python3*, *pip package installer*, *pgadmin4* and *postgresql* before running the project.

### Installation

* Clone the repo
   sh
   git clone {repository link}
   
* Open the migrations in home folder of the project and delete all the migration files which are numbered.
* Install postgresql and Pg-admin in your system.
* Create a database in pg admin.
* Update the database name and password in *settings.py* file of AMS folder to connect the database to our project.
* Change the directory to the place where manage.py file is available.
* Create a virtual environment
   * pip install virtualenvwrapper-win
   * mkvirtualenv 'name of your environment'
   
* Work on the created environment

   * workon 'name of your environment'
   
* Install the following pacakges using command prompt in the virtual environment
   
   * pip install django
   * pip install psycopg2
   * pip install face_recognition
   * pip install cmake
   
* Create django migrations for database using the following commands
   
   * python manage.py makemigrations
   * python manage.py sqlmigrate home 0001
   * python manage.py migrate
   
* Create a super user i.e, the admin
   
   python manage.py createsuperuser
   
   * The command prompt will ask for the username and password for the admin.
   * enter the required details
   
* Run the server and open the website at http://127.0.0.1:8000/ localhost
   
   python manage.py runserver
   
## Screenshots of the project running

![Screenshot (122)](https://user-images.githubusercontent.com/88847633/140688399-1b9873ed-d397-48c0-91ff-8e59b0fbff0e.png)

![Screenshot (123)](https://user-images.githubusercontent.com/88847633/140688428-7dc3db3d-43fb-49f1-a011-e441f0968545.png)

![Screenshot (124)](https://user-images.githubusercontent.com/88847633/140688466-30c48496-86d7-41e9-bba7-5b2893fb6647.png)

![Screenshot (125)](https://user-images.githubusercontent.com/88847633/140688502-3c6117ae-4adc-4e1a-a599-413b36afe6b1.png)




## Use Case Diagram
![image](https://user-images.githubusercontent.com/88847633/140704708-27dac304-5f17-4d31-8cb6-e702b320e088.png)

## Class Diagram
![uml Final class Diagram](https://user-images.githubusercontent.com/88847633/140705177-0929c592-1fff-494f-914e-4b3f26256674.jpeg)

## Sequence Diagrams

### LOGIN Sequence
![Untitled](https://user-images.githubusercontent.com/88847633/140706903-919cf1b4-7f1d-4c19-b920-93212367dc35.png)

### Time Table Access Sequence
![ams tt sequence](https://user-images.githubusercontent.com/88847633/140707115-70421e43-7c28-45f4-9015-4164181a4006.jpg)

### Queries Sequence
![WhatsApp Image 2021-10-26 at 12 27 26 PM](https://user-images.githubusercontent.com/88847633/140707332-bb484659-f9a9-4944-9b6b-bfdca9fd0d93.jpeg)

### Marking Attendance Sequence
![Sequence Diagram AMS (2)](https://user-images.githubusercontent.com/88847633/140707629-ec581ec7-1c67-4947-bbf9-71fbe121ba66.jpg)

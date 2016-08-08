# Django excel data analysis
* You can import excel sheet data to mysql using Django and Angular js.

## Examples
![Alt text](https://s7.postimg.org/v953oco2z/Screenshot_from_2016_08_07_01_56_27.png "Snapshot")
    
## Features
* This project makes it easy to:
  - Sort data by clicking their headings.
  - Filter data by using filter provided
  - Upload excel file to server and import it to mysql

## Installation

* Install [virtualenv](https://virtualenv.pypa.io/en/stable/) with the following command:
 
  ```sh
  $ pip install virtualenv
  ```
  
* Set up your development structure:
 
  ```sh
  $ mkdir YourProjectName
  $ cd YourProjectName
  $ virtualenv YourProjectEnv
  $ git clone git@github.com:ijajmulani/Djnago-file-upload-and-Analysis-of-data.git
  $ source YourProjectEnv/bin/activate
  $ cd risktask
  ```
  
* Let’s get Django installed:
  ```sh
  $ pip install django
  ```
  
* Install MySQL-python, which is a database connector for Python:
  ```sh
  $ pip install MySQL-python
  ```
* Install xlrd, The xlrd module reads a spreadsheet into a hierarchical data structure:
  ```sh
  $ pip install xlrd
  ```
  
* Edit your settings.py file within your  directory to add the following information about your database:
  ```
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.mysql',
      'NAME': 'django_db',
      'USER': 'root',
      'PASSWORD': 'your_password',
    }
  }
  ```
* Create your database tables:

  ```
  $ python manage.py migrate
  ```
* Launch the development server:
 
  ```
  $ python manage.py runserver
  ```

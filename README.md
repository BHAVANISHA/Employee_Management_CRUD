**Employee Management REST API Documentation**

**Overview**

This API provides CRUD functionality for managing employee records. It follows RESTful principles, ensures security via token-based authentication, and supports pagination, filtering, and error handling.

**Authentication**

In this I have implemented knox token based authentication for all the endpoints


**Requirements and Implementation**

Python, django, rest framework, mysql, mysql workbench, swagger or postman

**Create the django project:**

**Open the project in pycharm and set up the environment already created :** 

**Change the settings file with required details :** 

1.add app name,rest_framework, drf_yasg(swagger) in installed app 

2.set the database settings here I have used mysql for database connection via dbeaver mysql workbench

3.add authentication backend and swagger settings to display authentication setting in swagger.

**Inherit the knox file for implement authentication in django**

Download the knox file from the official github page and customise the name based on our project.

Give the custom settings for token authentication in settings.py 

**Implementation of API:**

**models.py:**

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission, Group




class UserManager( BaseUserManager ):
   def create_user(self,
                   user_email: str,
                   password: str,
                   is_staff=False,
                   is_superuser=True,
                   **extra_fields


                   ) -> "Users":
       if not user_email:
           raise ValueError( "User must have an email" )


       users = self.model( user_email=user_email, **extra_fields )
       users.set_password( password )
       users.is_active = True
       users.is_staff = is_staff
       users.is_superuser = is_superuser
       users.save()


       return users




   def create_superuser(
           self, user_email, password, **extra_fields
   ) -> "Users":
       extra_fields.setdefault( 'is_staff', True )
       extra_fields.setdefault( 'is_superuser', True )
       extra_fields.setdefault( 'is_active', True )
       users = self.create_user(
           user_email,
           password,
           **extra_fields
       )
       users.save()
       return users




class Users( AbstractUser ):
   username = models.CharField( max_length=255, null=True, blank=True )
   password = models.CharField( max_length=255 )
   last_login = models.DateTimeField( blank=True, null=True )
   is_superuser = models.IntegerField( null=True )
   first_name = models.CharField( max_length=100, blank=True, null=True )
   last_name = models.CharField( max_length=100, blank=True, null=True )
   email = models.CharField( max_length=254, null=True )
   is_staff = models.IntegerField(default=1)
   token = models.CharField( max_length=255, blank=True, null=True )
   is_active = models.IntegerField(default=1)
   date_joined = models.DateTimeField( auto_now_add=True )
   user_id = models.CharField( primary_key=True, default=None, max_length=10 )
   user_name = models.CharField( max_length=255, blank=True, null=True )
   user_phone = models.CharField( max_length=255, blank=True, null=True )
   status = models.CharField( max_length=255, null=True )
   is_verified = models.CharField( max_length=255,default=0 )
   reg_date = models.DateTimeField( auto_now_add=True )
   user_email = models.CharField( unique=True, max_length=255 )
   dob = models.DateField( blank=True, null=True )
   user_password = models.CharField( max_length=255 )
   gender = models.CharField( max_length=10, blank=True, null=True )
   first_login = models.IntegerField( blank=True, null=True )
   address = models.CharField( max_length=100, blank=True, null=True )
   city = models.CharField( max_length=100, blank=True, null=True )
   state = models.CharField( max_length=100, blank=True, null=True )
   postal_code = models.CharField( max_length=100, blank=True, null=True )
   country = models.CharField( max_length=100, blank=True, null=True )


   USERNAME_FIELD = 'user_email'
   REQUIRED_FIELDS = []
   objects = UserManager()


   # Override groups and user_permissions with unique related_name
   groups = models.ManyToManyField(
       Group,
       related_name='custom_user_groups',  # Custom related_name
       blank=True
   )
   user_permissions = models.ManyToManyField(
       Permission,
       related_name='custom_user_permissions',  # Custom related_name
       blank=True
   )


class Employee(models.Model):
   name = models.CharField(max_length=100, blank=False, null=False)
   email = models.EmailField(unique=True,blank=False)
   department = models.CharField(max_length=50, blank=True, null=True)
   role = models.CharField(max_length=50, blank=True, null=True)
   date_joined = models.DateField(auto_now_add=True)


class HabotAuthtoken( models.Model ):
   digest = models.CharField( primary_key=True, max_length=128 )
   token_key = models.CharField( max_length=8 )
   created = models.DateTimeField()
   expiry = models.DateTimeField( blank=True, null=True )
   user_id = models.CharField(max_length=12)




Here I have attached my models by defining Baseusermanager and AbstractUser  to customise the way users are created, particularly to handle fields differently from the default (like using email instead of username as the unique identifier).

**views.py:**

Step 1: First create the user for registration and login for authentication only authorised users can add the employee, edit the employee details, delete the employee and view the employee details.

Step 2: after login the custom knox token will be generated hashed and stored in the database 

This is the custom settings for knox token 
REST_KNOX = {
   'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',  # algorithm for hash the token
   'AUTH_TOKEN_CHARACTER_LENGTH': 128,  # character length of generated token
   'TOKEN_TTL': timedelta( hours=10 ),  # token expiry limit
  'USER_SERIALIZER': 'habot_employee_app.serializers.UserSignUpSerializer',
   # if we want to display employ details during login in response add that serializer
   'TOKEN_LIMIT_PER_USER': 1,
   'AUTO_REFRESH': False,
   'MIN_REFRESH_INTERVAL': 60,
   'AUTH_HEADER_PREFIX': 'Token',
   'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}

Step 3: only by this token the login user can add employee

**User Sign-Up**

Endpoint: POST /user_sign_up/

URL: http://127.0.0.1:8001/Habot_employee/logging/user_sign_up/

Description: Registers a new user account.

Required Fields:

first_name (string): User’s first name.

last_name (string): User’s last name.

dob (date): User’s date of birth.

gender (string): User’s gender.

user_email (string): User’s email address, must be unique.

password (string): User’s password.

Responses:

201 Created: User successfully registered.

400 Bad Request: Validation error if required fields are missing or email is not unique.

Sample request:
{
  "first_name": "alya",
  "last_name": "sigh",
  "dob": "2009-11-03",
  "gender": "female",
  "user_email": "alya@yahoo.com",
  "password": "123"
}

If the email already exists it shows error 

**User Login**

Endpoint: POST /user_login/

URL: http://127.0.0.1:8001/Habot_employee/logging/user_login/

Description: Authenticates a user and returns a token for accessing secure endpoints.

Required Fields:

user_email (string): Registered email of the user.

password (string): User’s password.

Responses:

200 OK: User successfully authenticated.

401 Unauthorised: Invalid credentials.

Sample Request:

{
  "user_email": "alya@yahoo.com",
  "password": "123"
}

**Create an Employee**

Endpoint: POST /add_employee/

URL: http://127.0.0.1:8001/Habot_employee/logging/add_employee/

Description: Adds a new employee to the database with unique email validation.

Required Fields:

name (string): The name of the employee.

email (string): The email address of the employee, must be unique.

Optional Fields:

department (string): The department of the employee, e.g., "HR", "Engineering", "Sales".

role (string): The role of the employee, e.g., "Manager", "Developer", "Analyst".

Auto-generated Fields:

id (integer): Unique identifier for each employee.

date_joined (date): Date of employee creation.

Responses:

201 Created: Employee successfully created.

400 Bad Request: Validation error if required fields are missing or email is not unique.

Sample request:

{
  "name": "bala",
  "email": "bala@gmail.com",
  "department": "HR",
  "role": "Manager"
} 

Give token as Token <your token>

**List Employees**

Endpoint: GET /list_employees/

URL: http://127.0.0.1:8001/Habot_employee/logging/list_employees/

Description: Fetches a list of employees with support for pagination and optional filtering by department or role.

Optional Query Parameters:

role (string): Filters employees by role.

department (string): Filters employees by department.

ordering (string): Field to use when ordering the results.

page (integer): Page number within the paginated result set.

page_size (integer): Number of results per page.

Responses:

200 OK: List of employees returned.

404 Not Found: No employees found for the specified filters.

Sample request:

{
  "role": "Analyst",
  "department": "HR",
  "ordering": "date_joined",
  "page":"10",
  "page_size":"2"
}

**Get Employee by ID**

Endpoint: GET /get_employee_by_id/{id}/

URL: http://127.0.0.1:8001/Habot_employee/logging/get_employee_by_id/{id}/

Description: Fetches employee details based on the provided employee ID.

Path Parameter:

id (integer): Unique identifier of the employee.

Responses:

200 OK: Employee details retrieved successfully.

404 Not Found: Employee ID not found.

Sample Request:

{
  "id": "4"
 
}

**Update Employee**

Endpoint: PUT /update_employee/

URL: http://127.0.0.1:8001/Habot_employee/logging/update_employee/

Description: Updates the details of an employee based on the provided employee ID.

Required Fields:

id (integer): Unique identifier of the employee.

Optional Fields:

name (string): Updated name of the employee.

email (string): Updated email address, must remain unique.

department (string): Updated department.

role (string): Updated role.

Responses:

200 OK: Employee details updated.

404 Not Found: Employee ID not found.

Sample request:
{
  "id": 1,
  "name": "rose",
  "email": "rose@gmail.com",
  "department": "HR",
  "role": "Analyst"
}

**Delete an Employee**

Endpoint: POST /delete_employee/

URL: http://127.0.0.1:8001/Habot_employee/logging/delete_employee/

Description: Permanently deletes employee records 

Required Fields:

id (integer): Unique identifier of the employee to delete.

Responses:

200 OK: Document successfully deleted.

404 Not Found: Employee ID not found.

Sample request:
{
  "id": 3
}

Note: All the test cases are checked All the API is used to written to handle all the testcases with proper status response.

For run this project clone this <git clone <project url>> create the environment install requirements to run this



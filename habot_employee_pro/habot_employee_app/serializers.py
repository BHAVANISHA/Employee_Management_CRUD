from django.contrib.auth import authenticate
from rest_framework import serializers
from django_filters import rest_framework as filters
from habot_employee_app import models


# -------------------------------signup
class UserSignUpSerializer( serializers.Serializer ):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    gender = serializers.CharField()
    user_email = serializers.CharField()
    password = serializers.CharField()


class UserSerializer( serializers.ModelSerializer ):
    class Meta:
        model = models.Users
        fields = (
            'user_email', 'password', 'first_name', 'last_name', 'dob', 'gender', 'user_id', 'user_name')

    def create(self, validated_data):
        user = models.Users.objects.create_user( **validated_data )
        return user


# --------------------------------------login

class UserLoginSerializer( serializers.Serializer ):
    user_email = serializers.CharField()
    password = serializers.CharField()


class LoginUserSerializer( serializers.Serializer ):
    user_email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False
    )

    def validate(self, data):
        user_email = data.get( 'user_email' )
        password = data.get( 'password' )

        if user_email and password:
            # Attempt authentication with user_email as username
            user = authenticate( username=user_email, password=password )
            if not user:
                raise serializers.ValidationError( {
                    'detail': 'Unable to log in with provided credentials.',
                    'register': True
                }, code='authorization' )
        else:
            raise serializers.ValidationError(
                'Must include "user_email" and "password".',
                code='authorization'
            )

        data['user'] = user
        return data


# ----------------------------------- add employees----------------------------


class AddEmployeeSerializer( serializers.ModelSerializer ):
    DEPARTMENT_CHOICES = [
        ('HR', 'HR'),
        ('Engineering', 'Engineering'),
        ('Sales', 'Sales'),
    ]
    ROLE_CHOICES = [
        ('Manager', 'Manager'),
        ('Developer', 'Developer'),
        ('Analyst', 'Analyst'),
    ]

    department = serializers.ChoiceField( choices=DEPARTMENT_CHOICES, required=False, allow_blank=True )
    role = serializers.ChoiceField( choices=ROLE_CHOICES, required=False, allow_blank=True )

    class Meta:
        model = models.Employee
        fields = ['name', 'email', 'department', 'role']


# -----------------------------------list employee

# FilterSet for filtering by role or department
class EmployeeFilter( filters.FilterSet ):
    role = filters.CharFilter( field_name="role", lookup_expr="iexact" )
    department = filters.CharFilter( field_name="department", lookup_expr="iexact" )

    class Meta:
        model = models.Employee
        fields = ['role', 'department']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = ['id', 'name', 'email', 'department', 'role', 'date_joined']

# ----------------------- get by id for employee details

class RetrieveSerializer(serializers.Serializer):
    id =serializers.IntegerField()

# ---------------------------update employee

class Employee_custom_Serializer(serializers.Serializer):
    id=serializers.IntegerField()
    name=serializers.CharField(required=False)
    email=serializers.CharField(required=False)
    department=serializers.CharField(default='HR',required=False)
    role = serializers.CharField(default='Analyst',required=False)


import random
import logging
import string

from django.contrib.auth import login
from django.db import IntegrityError
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, GenericAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters

from habot_employee_app.knox.auth import TokenAuthentication
from habot_employee_app import serializers, models
from habot_employee_app.knox.views import LoginView as KnoxLoginView

_logger = logging.getLogger( __name__ )


class UserSignUp( CreateAPIView ):
    ''' This class is used for User signup only sign in user access the employee details  '''

    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        try:
            user_id = 'USER_' + ''.join( random.choices( string.ascii_uppercase, k=6 ) )
            user_id = user_id[:10]
            name = request.data['first_name']
            request.data['user_id'] = user_id
            request.data['user_name'] = name
            serializer_class = serializers.UserSerializer( data=request.data )
            if serializer_class.is_valid():
                serializer_class.save()

                _logger.error( "user register successful" )
                return Response( {
                    'response_code': 200,
                    'message': 'User Signed up successfully',
                    'statusFlag': True,
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': serializer_class.data
                } )
            else:
                _logger.error( "User details is not valid" )
                return Response( {
                    'response_code': 400,
                    'message': 'User Signed up unsuccessful',
                    'statusFlag': False,
                    'status': 'FAILURE',
                    'errorDetails': 'Enter valid data',
                    'data': serializer_class.errors
                } )
        except Exception as e:
            _logger.error( "user_email already register" )
            return Response( {
                'response_code': 500,
                'message': str( e ),
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            } )


class UserLogin( KnoxLoginView, CreateAPIView ):
    '''This class is used for user login to generate the token by this token the user can add, edit,get, delete the employees'''
    serializer_class = serializers.UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            user_email = request.data.get( 'user_email' )
            # Check if the user exists
            if not models.Users.objects.filter( user_email=user_email ).exists():
                return Response( {
                    'response_code': 400,
                    "message": "Email is not registered",
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': "Email is not registered",
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST )

            # Validate login credentials
            serializer = serializers.LoginUserSerializer( data=request.data, context={'request': request} )
            serializer.is_valid( raise_exception=True )
            user = serializer.validated_data['user']

            # Log the user in and create a token
            login( request, user )
            response = super().post( request, format=None )
            # Success response with token
            _logger.info( "Logged in successfully. Token Generated" )
            return Response( {
                'response_code': 200,
                "message": "Token Generated Successfully",
                'statusFlag': True,
                'status': 'SUCCESS',
                'errorDetails': None,
                'data': response.data,

            } )

        except Exception as e:
            _logger.error( f"Login error: {str( e )}" )
            return Response( {
                'response_code': 500,
                "message": "The email ID or password you entered is incorrect. Please try again",
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


class AddEmployee( CreateAPIView ):
    '''This class is used to create an employee with unique email.'''
    serializer_class = serializers.AddEmployeeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        email = request.data.get( 'email' )

        try:
            # Check if email already exists in Employee table
            if models.Employee.objects.filter( email=email ).exists():
                return Response( {
                    'response_code': 400,
                    'message': 'Email is already registered in Employee table.',
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': {'user_email': 'This email is already in use.'},
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST )

            serializer = self.serializer_class( data=request.data )
            if serializer.is_valid():
                serializer.save()
                return Response( {
                    'response_code': 200,
                    'message': 'Employee created successfully',
                    'statusFlag': True,
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED )
            else:
                return Response( {
                    'response_code': 400,
                    'message': 'Employee creation failed',
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': serializer.errors,
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST )

        except IntegrityError as e:
            return Response( {
                'response_code': 400,
                'message': 'Database Integrity Error. Duplicate email or other constraint.',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST )

        except Exception as e:
            return Response( {
                'response_code': 500,
                'message': 'An unexpected error occurred.',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


# -------------------------list the employee

# Custom pagination class
class CustomPagination( PageNumberPagination ):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListEmployees( GenericAPIView ):
    '''Fetch employee details with pagination and filtering by role or department'''

    serializer_class = serializers.EmployeeSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = serializers.EmployeeFilter
    ordering_fields = ['name', 'date_joined']
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request, *args, **kwargs):
        try:
            # Get the initial queryset
            queryset = models.Employee.objects.all()
            filterset = serializers.EmployeeFilter( request.GET, queryset=queryset )
            if filterset.is_valid():
                queryset = filterset.qs
            else:
                _logger.warning( "Invalid filter parameters provided." )
                return Response( {
                    'response_code': 400,
                    'message': 'Invalid filter parameters',
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': filterset.errors,
                    'data': []
                } )

            # Paginate the queryset
            paginator = CustomPagination()
            paginated_queryset = paginator.paginate_queryset( queryset, request )
            serializer = serializers.EmployeeSerializer( paginated_queryset, many=True )

            _logger.info( "Employee data fetched successfully." )
            return paginator.get_paginated_response( {
                'response_code': 200,
                'message': 'Employee details fetched successfully',
                'statusFlag': True,
                'status': 'SUCCESS',
                'errorDetails': None,
                'data': serializer.data
            } )

        except Exception as e:
            _logger.error( "Employee fetching process failed." )
            return Response( {
                'response_code': 500,
                'message': 'Employee fetching failed',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            } )


# ------------------------get by id employee details -----------------------

class RetrieveEmployeeById( GenericAPIView ):
    '''Fetch employee details by ID'''
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]
    def get(self, request, **kwargs):
        try:
            employee = models.Employee.objects.filter( id=kwargs['id'] )
            serializer = serializers.EmployeeSerializer( employee, many=True )
            if serializer.data:
                _logger.info( "Employee data has been fetched successfully." )
                return Response( {
                    'response_code': 200,
                    'message': 'Employee details fetched successfully',
                    'statusFlag': True,
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': serializer.data
                } )
            else:
                _logger.error( "Employee not found with the specified ID." )
                return Response( {
                    'response_code': 404,
                    'message': 'Employee not found',
                    'statusFlag': False,
                    'status': 'FAILED',
                    'errorDetails': 'Employee not found with the specified ID',
                    'data': []
                } )

        except Exception as e:
            _logger.error( "Fetching employee process failed." )
            return Response( {
                'response_code': 500,
                'message': 'An unexpected error occurred.',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            } )


class UpdateEmployee( UpdateAPIView ):
    '''This class is used to update an employee's details by ID'''
    serializer_class = serializers.Employee_custom_Serializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def put(self, request, *args, **kwargs):
        try:
            # Find employee by ID
            id = request.data['id']
            if id:
                instance = models.Employee.objects.get( id=request.data['id'] )
                if instance:
                    # Update the instance with the received data using Recipient_listSerializer
                    serializer_data = serializers.EmployeeSerializer( instance=instance, data=request.data,
                                                                      partial=True )
                    if serializer_data.is_valid():
                        self.perform_update( serializer_data )

                        _logger.info( "Employee details have been updated successfully." )

                        return Response( {
                            'responseCode': 200,
                            'message': 'Updated successfully',
                            'statusFlag': True,
                            'status': 'SUCCESS',
                            'errorDetails': None,
                            'data': serializer_data.data
                        }, status=status.HTTP_200_OK )

                    return Response( {
                        'responseCode': 404,
                        'message': 'Employee not found',
                        'statusFlag': False,
                        'status': 'FAILED',
                        'errorDetails': 'No employee found with the specified ID',
                        'data': []
                    }, status=status.HTTP_404_NOT_FOUND )

            return Response( {
                'responseCode': 400,
                'message': 'Update failed',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': 'id not found',
                'data': []
            }, status=status.HTTP_400_BAD_REQUEST )

        except Exception as e:
            _logger.error( "An error occurred while updating the employee details." )
            return Response( {
                'responseCode': 500,
                'message': "Couldn't update the employee's details.",
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR )


# ---------------------------delete employee by id-------------------

class DeleteEmployee( GenericAPIView ):
    '''This class used to delete the already deleted documents in the (deleted documents) table after 30 days'''
    serializer_class = serializers.RetrieveSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        try:
            # Filter the deleted documents older than 30 days
            emlpoyee = models.Employee.objects.filter(
                id=request.data['id'] )
            if emlpoyee:
                # Delete employee
                emlpoyee.delete()

                _logger.info( "Employee deleted successfully." )
                data = {
                    'response_code': 200,
                    'message': 'Employee deleted successfully',
                    'statusFlag': True,
                    'status': 'SUCCESS',
                    'errorDetails': None,
                    'data': []
                }
                return Response( data )
            _logger.error( "Failed to delete employee")
            data = {
                'response_code': 404,
                'message': 'employee not found',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': 'id not found',
                'data': []
            }
            return Response( data )
        except Exception as e:
            _logger.error( "Failed to delete Employee: %s", str( e ) )
            data = {
                'response_code': 500,
                'message': 'Failed to delete employee',
                'statusFlag': False,
                'status': 'FAILED',
                'errorDetails': str( e ),
                'data': []
            }
            return Response( data )

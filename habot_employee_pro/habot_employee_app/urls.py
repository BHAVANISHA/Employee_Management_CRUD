from habot_employee_pro import swagger_service
from django.urls import path, include
from habot_employee_app import views
urlpatterns = [

    path('docs/', swagger_service.schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),


    path('logging/', include([
        path('', include([

            path( 'user_sign_up/', views.UserSignUp.as_view() ),
            path('user_login/',views.UserLogin.as_view()),
            path('add_employee/',views.AddEmployee.as_view()),
            path('list_employees/',views.ListEmployees.as_view()),
            path('get_employee_by_id/<int:id>/',views.RetrieveEmployeeById.as_view()),
            path('update_employee/',views.UpdateEmployee.as_view()),
            path('delete_employee/',views.DeleteEmployee.as_view())


        ]))
    ])),]
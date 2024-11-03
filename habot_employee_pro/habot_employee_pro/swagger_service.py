import socket
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

# Get the hostname and IP address
hostname = socket.gethostname()
try:
    # Ensure IP address is properly retrieved
    IPAddr = socket.gethostbyname(hostname)
except socket.gaierror:
    # Fallback IP address in case of error
    IPAddr = "15.207.242.99"

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a Swagger object with custom tags."""
        swagger = super().get_schema(request, public)
        swagger.tags = [
            # Add tags here as needed, e.g.,
            # {
            #     "name": "logging",
            #     "description": "Operations related to account registration, login, and logout."
            # },
        ]
        return swagger

# Custom content for the Swagger description
content = "Habot"

# Schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Habot Employee API",
        default_version='v1',
        description=(
            f"Description: {content}\n\n"
            f"Logfile Link: http://{IPAddr}/habot.log\n\n"
            "Environment - Dev"
        ),
        terms_of_service="https://www.habot.com/",
        contact=openapi.Contact(email="xxxx@habot.com"),
        license=openapi.License(name="habotConnect"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=CustomOpenAPISchemaGenerator,
)

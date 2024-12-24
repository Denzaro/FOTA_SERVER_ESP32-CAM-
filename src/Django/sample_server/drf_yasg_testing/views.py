from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class HelloWorld(APIView):
    """
    A simple API view.
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('message', openapi.IN_QUERY, description="Message to be echoed back", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the sender", type=openapi.TYPE_STRING),
        ],
        operation_summary="Get a simple hello message with parameters."
    )
    def get(self, request):
        """
        Get a simple hello message.
        """
        message = request.GET.get('message')
    
        return Response(data={"message": message}, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description='Message to be echoed back'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the sender'),
            }
        ),
        operation_summary="Echo back the message sent in the request body.",
        responses={200: "Success response description"},
    )
    def post(self, request):
        """
        Echo back the message sent in the request body.
        """
        message = request.data.get('message', '')
        name = request.data.get('name', '')
        response_data = {
            "message": message,
            "name": name
        }
        return Response(data=response_data, status=status.HTTP_200_OK)
    
    # Define Swagger schema directly within the methods
   
    
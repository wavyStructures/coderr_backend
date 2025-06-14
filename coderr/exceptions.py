from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status
import traceback

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        print("\n🔥 Unhandled DRF Exception 🔥")
        print(traceback.format_exc())
        print("Exception type:", type(exc).__name__)
        print("Exception message:", str(exc))
        return Response({
            'error': 'An unexpected error occurred',
            'detail': str(exc),
            'type': type(exc).__name__,
        }, status=500)
 
          
    if isinstance(exc, NotAuthenticated):
        return Response(
            {"detail": "NotAuthenticated"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    elif isinstance(exc, PermissionDenied):
        return Response(
            {"detail": "PermissionDenied"},
            status=status.HTTP_403_FORBIDDEN
        )

    elif isinstance(exc, NotFound):
        return Response(
            {"detail": "NotFound"},
            status=status.HTTP_404_NOT_FOUND
        )

    elif isinstance(exc, ValidationError):
        return Response(
            {"detail": "ValidationError"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # elif isinstance(exc, APIException):
    #     return Response(
    #         {"detail": "APIException"},
    #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #     )

    return response

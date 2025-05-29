# coderr/exceptions.py

from rest_framework.views import exception_handler
from rest_framework.response import Response
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

    return response

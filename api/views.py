from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
API_ENDPOINT = os.getenv('API_ENDPOINT')
API_AUTH = os.getenv('API_AUTH')

@api_view(['GET'])
def get_api_data(request):
    # Force JSON renderer only
    request.accepted_renderer = JSONRenderer()
    
    try:
        # Step 1: Authenticate and get token
        auth_payload = {
            'email': EMAIL,
            'password': PASSWORD
        }
        
        auth_response = requests.post(API_AUTH, json=auth_payload)
        auth_response.raise_for_status()
        
        # Extract token from auth response
        token = auth_response.json().get('access')
        
        if not token:
            return JsonResponse({'error': 'Authentication failed - no token received'}, status=401)
        
        # Step 2: Make request to API endpoint with token
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        api_response = requests.get(API_ENDPOINT, headers=headers)
        api_response.raise_for_status()
        
        # Return the API response data as JSON
        return JsonResponse(api_response.json(), safe=False)
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"API request failed: {str(e)}"}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
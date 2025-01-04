from django.http import JsonResponse
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from dotenv import load_dotenv
import os
from api.models import Medicament
load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
API_ATTENTE = os.getenv('API_ATTENTE')
API_AUTH = os.getenv('API_AUTH')
API_NONVALIDE = os.getenv('API_NONVALIDE')
API_VALIDE = os.getenv('API_VALIDE')



def validate_medicament(medicament_data):
    """Validate the medicament's dose, duration, and stock."""
    medicament = Medicament.objects.filter(nom=medicament_data['Medicament']['nom']).first()
    if not medicament:
        return False

    # Check dose
    if medicament_data['dose'] > medicament.max_dose:
        return False

    # Check duration
    if medicament.max_duree > 0 and medicament_data['duree'] > medicament.max_duree:
        return False

    # Check stock
    if not medicament.in_stock:
        return False

    return True


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
        
        response = requests.get(API_ATTENTE, headers=headers)
        if response.status_code != 200:
             return JsonResponse({'error': 'Failed to fetch ordonnances'}, status=500)

        ordonnances = response.json()
        validated_ids = []
        non_validated_ids = []
        for ordonnance in ordonnances:
          is_valid = all(validate_medicament(med) for med in ordonnance['medicaments'])
          if is_valid:
            validated_ids.append(ordonnance['IdOrdonnance'])
          else:
            non_validated_ids.append(ordonnance['IdOrdonnance'])
        
            # Update ordonnances' statuses
        # for ordonnance_id in validated_ids:
        #  requests.put(f"{API_VALIDE}/{ordonnance_id}", headers=headers)

        # for ordonnance_id in non_validated_ids:
        #  requests.put(f"{API_NONVALIDE}/{ordonnance_id}", headers=headers)

        return JsonResponse({
        'validated': validated_ids,
        'non_validated': non_validated_ids
            })

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"API request failed: {str(e)}"}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
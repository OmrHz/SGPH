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
        results = []

        for ordonnance in ordonnances:
            is_valid = True
            total_prix = 0
            reasons = []

            for med in ordonnance['medicaments']:
                medicament = Medicament.objects.filter(id=med['Medicament']['IdMedicament']).first()

                if not medicament:
                    is_valid = False
                    reasons.append(f"Medicament ID {med['Medicament']['IdMedicament']} does not exist.")
                    continue

                # Check dose
                if med['dose'] > medicament.max_dose:
                    is_valid = False
                    reasons.append(
                        f"Medicament '{medicament.nom}' exceeds max dose. Given: {med['dose']}, Max: {medicament.max_dose}."
                    )

                # Check duration
                if medicament.max_duree > 0 and med['duree'] > medicament.max_duree:
                    is_valid = False
                    reasons.append(
                        f"Medicament '{medicament.nom}' exceeds max duration. Given: {med['duree']} days, Max: {medicament.max_duree} days."
                    )

                # Check stock
                if not medicament.in_stock:
                    is_valid = False
                    reasons.append(f"Medicament '{medicament.nom}' is out of stock.")

                # Add price if valid so far
                if is_valid:
                    total_prix += medicament.prix

            # Add results for this ordonnance
            results.append({
                'IdOrdonnance': ordonnance['IdOrdonnance'],
                'is_valid': is_valid,
                'prix': total_prix if is_valid else None,
                'reasons': reasons if not is_valid else None
            })

        # Update ordonnance status via API
        # if is_valid:
        #     requests.put(f"{API_VALIDE}/{ordonnance['IdOrdonnance']}", headers=headers)
        # else:
        #     requests.put(f"{API_NONVALIDE}/{ordonnance['IdOrdonnance']}", headers=headers)

        return JsonResponse({'results': results}, safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"API request failed: {str(e)}"}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

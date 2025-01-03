from 
API_KEY = 'your_secure_api_key'
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://hospital-dpi-system.com/api/prescriptions/patient/123',
    headers=headers
)
import os
import json
import requests

def authenticate_api_key():
    """Authenticate API key using information from .credential file."""
    credential_path = os.path.join(os.getcwd(), '.credential')
    session_path = os.path.join(os.getcwd(), '.lum0x_session')

    if os.path.exists('.credential'):
        with open(credential_path, 'r') as credential_file:
            creds = json.load(credential_file)
    else:
        print("Error: .credential file not found.")
        return

    try:
        auth_payload = {
            "farcasterFid": creds["FARCASTER_ID"],
            "api_key": creds["LUM0X_API_KEY"]
        }
        response = requests.post("https://testnetapi.lum0x.com/keys/authentication", json=auth_payload)

        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        if response.status_code in [200, 201]:
            data = response.json()
            with open(session_path, 'w') as session_file:
                json.dump({
                    'farcasterFid': creds['FARCASTER_ID'],
                    'api_key': creds['LUM0X_API_KEY'],
                    'authenticatedAt': data['authenticatedAt'],
                    'aws_access_key_id': creds['AWS_ACCESS_KEY_ID'],
                    'aws_secret_access_key': creds['AWS_SECRET_ACCESS_KEY'],
                    'aws_region': creds['AWS_REGION'],
                    'aws_lambda_role_arn': creds['AWS_LAMBDA_ROLE_ARN']
                }, session_file)

            print(f"API key validated and saved. Farcaster FID: {data['farcasterFid']}")
        else:
            print("Invalid API key.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

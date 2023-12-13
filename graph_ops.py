import requests
import argparse
import sys

# Get authentication token for GRAPH
def get_token(args: argparse.Namespace) -> str: 

    client_id = args.clientId
    client_secret = args.clientSecret
    tenant_id = args.tenantId

    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }

    token_r = requests.post(token_url, data=token_data)
    token = token_r.json().get("access_token")

    if token is None:
        print("Failed to get authentication token...")
        print("Ensure that the Client ID, Client Secret and Tenant ID are correct...")
        sys.exit(1)

    else:
        return token

def build_auth_headers(token): 
    
    auth_headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    return auth_headers

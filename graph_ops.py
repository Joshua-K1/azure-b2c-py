import requests
import argparse
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import sys

# Get authentication token for GRAPH
def get_token(args: argparse.Namespace) -> str: 
    token = ""

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

    try:
        token_r = requests.post(token_url, data=token_data)
        token = token_r.json().get("access_token")
    except HTTPError as http_error: 
        print(f'HTTP Error occurred:{http_error}')
    except ConnectionError as conn_error: 
        print(f'Connection Error occurred:{conn_error}')
    except Timeout as timeout_error: 
        print(f'Timeout Error occurred:{timeout_error}')
    except RequestException as req_error: 
        print(f'Request Error occurr:{req_error}')

    return token

def build_auth_headers(token: str) -> dict:
    
    auth_headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    return auth_headers

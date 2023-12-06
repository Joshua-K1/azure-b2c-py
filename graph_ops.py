import requests

def get_token(args): 
    
    client_id = args.clientId
    client_secret = args.clientSecret
    tenant_id = args.tenantId

    # Get an access token
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    
    token_r = requests.post(token_url, data=token_data)
    token = token_r.json().get("access_token")

    return token

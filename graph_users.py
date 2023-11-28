from email import header
from operator import indexOf
import requests
import time
import csv

# Replace these with your app reg details
client_id = ''
client_secret = ''
tenant_id = ''

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

# Iniial URL, uncomment on first run
continuation_url = 'https://graph.microsoft.com/v1.0/users?$select=signInActivity&$top=999'

for x in range(25):
    f = open("continuation_url_log", "a")
    f.write(continuation_url)
    f.write("\n")
    
    print("Continuation URL at beginning of loop: ", continuation_url)
    # Make a request to the Microsoft Graph API
    graph_all_users = continuation_url
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # GET response
    graph_all_users_r = requests.get(graph_all_users, headers=headers)

    # Process the response
    users = graph_all_users_r.json()

    # Retrieve User Dict
    user_list = users["value"]
   
    if '@odata.nextLink' in users:
        continuation_url = users["@odata.nextLink"]
    else: 
        continuation_url = 'None'

    print("URL taken from response: ", continuation_url)

    user_id_arr = []
    user_principle_name_arr = []
    user_sign_signn_activity_arr = []
    user_objects_arr = []
    count = 0

    # Iterate through each user in user_list dict
    for user in user_list:
        if 'signInActivity' in user:
            sign_in = user['signInActivity']
            user_sign_signn_activity_arr.append(sign_in['lastSignInDateTime'])
        else:
            user_sign_signn_activity_arr.append('None')

        user_principle_name_arr.append(user['userPrincipalName'])
        user_id_arr.append(user['id'])
        user_id_s = user['id']
        
    # Iterate through each UPN and get identities object
    for user_principle_name in user_principle_name_arr:
        
        id_index = user_principle_name_arr.index(user_principle_name)   
        f_user_id = user_id_arr[id_index]
        f_user_sign_in = user_sign_signn_activity_arr[id_index]

        graph_user_principal = f'https://graph.microsoft.com/v1.0/users/{f_user_id}?$select=identities'
        
        # GET
        graph_user_principal_r = requests.get(graph_user_principal, headers=headers)
        identities = graph_user_principal_r.json()
        print(identities)
        count += 1
        print("Got Id: ", count)

        user_identity = identities["identities"]

        if len(user_identity) > 1: 
            user_identity_a = user_identity[0]
            f_user_identity_a_s = user_identity_a["issuerAssignedId"]
            print(f_user_identity_a_s)

            user_identity_b = user_identity[1]
            f_user_identity_b_s = user_identity_b["issuerAssignedId"]
            print(f_user_identity_b_s)
        else:
            user_identity_a = user_identity[0]
            f_user_identity_a_s = user_identity_a["issuerAssignedId"]
            print(f_user_identity_a_s)

            user_identity_b = 'None'

        user_info = {
            "Id": f_user_id,
            "Email": f_user_identity_a_s,
            "UserPrin": f_user_identity_b_s,
            "SignIn": f_user_sign_in
        }

        user_objects_arr.append(user_info)
        #print(user_info)

        print("-------")
        print("\n")

    csv_file_name = 'output.csv'

    fieldnames = user_objects_arr[0].keys()

    with open(csv_file_name, mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write the headers
        writer.writeheader()

        # Write the data rows
        for row in user_objects_arr:
            writer.writerow(row)

    print(f"Data written to {csv_file_name}")

import requests
import argparse
import csv
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from graph_ops import get_token, build_auth_headers

# TODO: 
# Create user class

# List all users within the tenant
def list_all(args: argparse.Namespace) -> None:
    token = get_token(args)

    # Iniial URL, uncomment on first run
    continuation_url = 'https://graph.microsoft.com/v1.0/users?$select=signInActivity&$top=999'

    for x in range(25):
        
        # Opening continuation_url as log file
        f = open("continuation_url.log", "a")
        f.write(continuation_url)
        f.write("\n")
        
        # print("Continuation URL at beginning of loop: ", continuation_url)
    
       # Add continuation_url if it has changed whilst in the loop 
        graph_all_users = continuation_url
      
        headers = build_auth_headers(token)

        # Perform request to GRAPH API
        graph_all_users_r = requests.get(graph_all_users, headers=headers)

        # Process the response
        users = graph_all_users_r.json()

        # Retrieve User Dict
        user_list = users["value"]

        # Results from GRAPH are paginated
        if '@odata.nextLink' in users:
            continuation_url = users["@odata.nextLink"]
        else: 
            continuation_url = 'None'

        #print("URL taken from response: ", continuation_url)

        user_id_arr = []
        user_principle_name_arr = []
        user_sign_signn_activity_arr = []
        user_objects_arr = []

        # Iterate through each user in user_list dict
        for user in user_list:

            # Check for signInActvity 
            if 'signInActivity' in user:
                sign_in = user['signInActivity']
                user_sign_signn_activity_arr.append(sign_in['lastSignInDateTime'])
            else:
                user_sign_signn_activity_arr.append('None')

            user_principle_name_arr.append(user['userPrincipalName'])
            user_id_arr.append(user['id'])
            
        # Iterate through each UPN and get identities object
        for user_principle_name in user_principle_name_arr:
            # Gets the index of the current user_principle_name 
            id_index = user_principle_name_arr.index(user_principle_name)
            f_user_id = user_id_arr[id_index]
            f_user_sign_in = user_sign_signn_activity_arr[id_index]

            # GET: indentities of user
            graph_user_principal = f'https://graph.microsoft.com/v1.0/users/{f_user_id}?$select=identities'
            
           
            # GET
            graph_user_principal_r = requests.get(graph_user_principal, headers=headers)
            identities = graph_user_principal_r.json()

            user_identity = identities["identities"]
        
            # if user_identity object is greater than 1
            if len(user_identity) > 1: 
                # Get issuerAssignedId value at position 0 of user_identity array
                user_identity_a = user_identity[0]
                f_user_identity_a_s = user_identity_a["issuerAssignedId"]

                # Get issuerAssignedId value at position 1 of user_identity array
                user_identity_b = user_identity[1]
                f_user_identity_b_s = user_identity_b["issuerAssignedId"]

            # if user_identify object is less than 1
            else:
                # Get issuerAssignedId value at position 0 of user_identity array
                user_identity_a = user_identity[0]
                f_user_identity_a_s = user_identity_a["issuerAssignedId"]
                user_identity_b = 'None'
            
            # Create user_info object
            user_info = {
                "Id": f_user_id,
                "Email": f_user_identity_a_s,
                "UserPrin": f_user_identity_b_s,
                "SignIn": f_user_sign_in
            }
          
            print(user_info)
            # append user object info to user array
            user_objects_arr.append(user_info)

            print("-------")
            print("\n")

        csv_file_name = 'output.csv'
        
        # field names of the csv file will be the first value in the user object array
        fieldnames = user_objects_arr[0].keys()

        # write values to csv file
        with open(csv_file_name, mode='a', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write the headers
            writer.writeheader()

            # Write the data rows
            for row in user_objects_arr:
                writer.writerow(row)

        print(f"Data written to {csv_file_name}")

# List details of a specific user
def list_user_details(args: argparse.Namespace) -> None:

    token = get_token(args)
    headers = build_auth_headers(token)

    user_principle_name = args.userPrin

    spec_user_req = f'https://graph.microsoft.com/v1.0/users/{user_principle_name}'

    try:
        spec_user_res = requests.get(spec_user_req, headers=headers)
        print(spec_user_res)
    except HTTPError as http_error: 
        print(f'HTTP Error occurred:{http_error}')
    except ConnectionError as conn_error: 
        print(f'Connection Error occurred:{conn_error}')
    except Timeout as timeout_error: 
        print(f'Timeout Error occurred:{timeout_error}')
    except RequestException as req_error: 
        print(f'Request Error occurr:{req_error}')


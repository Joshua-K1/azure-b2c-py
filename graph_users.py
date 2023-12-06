import requests
import csv
import argparse 
from user_ops import list_all

def main(args):

    if args.listAll: 
        list_all(args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Process external arguments")
    
    parser.add_argument("-clientId", type=str, required=True, help="The Client ID")
    parser.add_argument("-clientSecret", type=str, required=True, help="The Client Secret")
    parser.add_argument("-tenantId", type=str, required=True, help="The Tenant ID")
    parser.add_argument("-listAll", action="store_true", help="List all users")

    args = parser.parse_args()

    main(args)





import json
import boto3
import sys

client = boto3.client('workspaces', region_name='us-west-2')


def get_dir_id_and_regcode_for_user(username, list_of_directories):

# In this function, we return the first directory ID/reg code that has a workspace for the user

    for directory in list_of_directories:
        try:
            print("Checking directory "+directory[0])
            response = client.describe_workspaces(
                DirectoryId=directory[0],
                UserName=username
            )
            #print(response)
            #print(len(response["Workspaces"]))
            if(len(response["Workspaces"]) > 0):
                print("Found a workspace!")
                return [directory[0], directory[1]]
            else:
                print("No WorkSpaces for user "+username+" in directory " + directory[0])
        except:
            print("There was an error when calling directory " + directory[0])
            print("Unexpected error:", sys.exc_info()[0])

    directoryID = "test"
    regCode = "test"

    return []


def get_mfa_code_for_user():

    return "123231"

def construct_workspace_uri(username, directoryID, regCode,mfa_otp):
    uri = "workspaces://"+username+"@"+regCode+"?MFACode="+mfa_otp
    #uri = "workspaces://"+username+"@"+regCode

    return uri

def get_list_of_workspace_directories():

    # Get a list of all workspaces in the directory
    response = client.describe_workspace_directories()
    directories = []

    for directory in response["Directories"]:
        directoryID = directory["DirectoryId"]
        regCode = directory["RegistrationCode"]

        #Appends a tuple to the directories list. Each tuple contains the directory ID and reg code.
        directories.append([directoryID,regCode])

    #print ("Directories found: "+str(len(directories)))
    return directories


def lambda_handler(event, context):
    # TODO implement
    
    username = event["username"]

    list_of_directories = get_list_of_workspace_directories()
    
    if(len(list_of_directories) < 1):
        return {
            "statusCode": 500,
            "errorMessage" : "No registered Directories found in your account."
        } 
    
    users_directory = get_dir_id_and_regcode_for_user(username,list_of_directories)

    if(len(users_directory) < 1):
        return {
            "statusCode": 500,
            "errorMessage" : "No WorkSpaces Found for user "+username
        } 
    
    users_directory = get_dir_id_and_regcode_for_user(username,list_of_directories)
    
    print("Directory for user "+username+" is "+users_directory[0])
    print("Reg Code for user "+username+" is "+users_directory[1])
    
    
    uri = construct_workspace_uri(username, users_directory[0], users_directory[1],"123121")
    
    print(uri)
    
    return {
        "statusCode": 200,
        "uri": uri
    }
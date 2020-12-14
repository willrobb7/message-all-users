import json
import logging
import os
import urllib
from typing import List
# import boto3
import requests
from requests.auth import HTTPBasicAuth
from slack_api import Slack

from util import get_secret



logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



secrets = json.loads(get_secret("message-all-users/secrets"))
logger.info(secrets)
bamboo_domain = secrets.get("BAMBOO_DOMAIN")

bamboo_reports_url = f"https://api.bamboohr.com/api/gateway.php/{bamboo_domain}/v1/reports/custom"
bamboo_api_key = secrets.get("BAMBOO_API_KEY")
bamboo_auth = HTTPBasicAuth(bamboo_api_key, "x")

slack_token = secrets.get('SLACK_TOKEN')

# with statement is a context manager
# with open("message_format.json", "r") as json_file:
#     message_format = json.loads(json_file.read())

#List of users to message goes into 'lll' in CSV format.
lll = [
'will.robinson@infinityworks.com',
]



#
# def process_event(event):
#     params = urllib.parse.unquote_plus(urllib.parse.unquote_plus(event['body']))
#     params = json.dumps(params)[9:][:-1].replace("\\", "")
#     params = json.loads(params)
#
#     return params




def lambda_handler(event, context):  # Initiating Lambda entry point
    bamboo_data = get_bamboo_employees()
    # print(bamboo_data)
    # process_employees()
    # incoming_data = json.loads(event.get("body"))
    incoming_data = bamboo_data[0]
    # logger.info(list_of_emails)
    # users_to_message = process_incoming_data(incoming_data, bamboo_data)
    users_to_message = process_incoming_data(lll)
    process_employees(users_to_message)

    # logger.info(users_to_message)

    return {
        'statusCode': 200,
        'body': json.dumps('All Good!')
    }




# def process_incoming_data(data: List[dict], bamboo_data: dict):
def process_incoming_data(lll: List[dict]):
    emails = list()
    for employee in lll:
        emails.append(employee)
    # for employee in data:
    #     # print(employee)
    #     for bamboo_employee in bamboo_data:
    #         name = f"{bamboo_employee.get('firstName')} {bamboo_employee.get('lastName')}"
    #         if bamboo_employee.get("status").lower() != "active":
    #             # logger.info(f"Skipping bamboo user {bamboo_employee} due to being inactive")
    #             continue
    #         surname = bamboo_employee.get("lastName")
    #         preferred_name = bamboo_employee.get('preferredName')
    #
    #         full_preferred_name = None
    #         full_name = f"{bamboo_employee.get('firstName')} {surname}".lower()
    #
    #         if preferred_name:  # Checking preferred_name is not None
    #             full_preferred_name = f"{preferred_name} {surname}".lower()
    #
    #         if name.lower() == full_name or name.lower() == full_preferred_name:
    #             email = bamboo_employee.get("workEmail")
    #             # logger.info(f"Appending {bamboo_employee}")
    #
    #             emails.append(email)



    return set(emails)


def get_bamboo_employees():
    response = requests.post(
        url=bamboo_reports_url,
        headers={"content-type": "application/json"},
        params={"format": "JSON"},
        data=json.dumps({
            "title": "Work Email please",

            "fields": [
                "status",
                "firstName",
                "preferredName",
                "lastName",
                "workEmail"
            ]
        }),
        auth=bamboo_auth
    )

    response.raise_for_status()

    return response.json().get("employees")



def process_employees(employees: set):
    slack_client = Slack(token=slack_token)
    number =0
    for employee in employees:
        # employeeString = str(employee)
        # if employeeString == "will.robinson@infinityworks.com" or employeeString == "tim.slow@infinityworks.com" :
        #     slack_client.message_user(employee,day4)
        # logger.info(employee)
        number = number + 1
        try:
            #Uncomment the line below to actually send a message to the users. Also create a varaiable for Message to say whatever you want
            # slack_client.message_user(employee,Message)
            logger.info(f"Should be messaging {employee}")
            logger.info(number)
        except:
            logger.info(f"EXECUTION FAILED: {employee} not messaged!")
            pass
            # logger.info(employee)
        # logger.info(f"Should be messaging {employee}")
        # slack_client.message_user(employee, "Is your address correct in BambooHR?", blocks=message_format)



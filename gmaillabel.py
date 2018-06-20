"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import pdb

# Setup the Gmail API
SCOPES = 'https://mail.google.com/,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.metadata'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    print(dir(flow));
    creds = tools.run_flow(flow, store)
print('creds:',creds)
service = build('gmail', 'v1', http=creds.authorize(Http()))

profile = service.users().getProfile(userId='me').execute()
print (profile['emailAddress'])

request = {
  'labelIds': ["INBOX"],
  'topicName': "projects/gmail-filing/topics/labelchange"
}


# Call the Gmail API

response = service.users().messages().list(userId="me",q='label:kris').execute()
messages = []
print ("response :",response)
if 'messages' in response:
    messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      print ("page_token:",page_token)
      response = service.users().messages().list(userId="me",q='label:trip',pageToken=page_token).execute()
      messages.extend(response['messages'])

for m in messages:
    message = service.users().messages().get(userId='me', id=m['id']).execute()
    print ("Message: ",message['snippet'])


response = service.users().watch(userId=profile['emailAddress'], body=request).execute()
print (response)

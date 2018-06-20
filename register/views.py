from __future__ import print_function
from django.shortcuts import render
from django.http import HttpResponse
import zeep
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from gmail import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from register.models import CredentialsModel
import httplib2
#import google.oauth2.credentials
#import google_auth_oauthlib.flow



import pdb

#flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
#          'client_secrets.json', 
#           scope=['https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.metadata'],
#
#          )


FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope=['https://mail.google.com/','https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.metadata'],
    redirect_uri='http://localhost:8000/oauth2callback')


@login_required
def auth_return(request):
  print ('request get: ',request.GET['state'],request.user)

  a = xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'].encode(),
                                 request.user)
  print ('a:',a)
  if not a:
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.GET)
  print ('credential:', credential)
  storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
  print ('storage:',storage)
  storage.put(credential)
  return HttpResponseRedirect("/home")



def getlist(list):
    filereferencelist=[]
    for i in list:
        fileRefTitle=''
        documentCount=''
        securityGrading=''
        fileRefNo=''
        compartment = i['compartment']
        caseRefs = i['caseRefs']

	 #   print ('List element: ', i,)
        for rowelement in i['_raw_elements']:
            if rowelement.tag == 'fileRefTitle':
                fileRefTitle = rowelement.text
            if rowelement.tag == 'documentCount':
                documentCount = rowelement.text
            if rowelement.tag == 'securityGrading':
                securityGrading = rowelement.text
            if rowelement.tag == 'fileRefNo':
                fileRefNo = rowelement.text
        if compartment is None: 
            compartment =''
        if fileRefTitle is None: 
            fileRefTitle=''
        if fileRefNo is None: 
            fileRefNo=''

        fl = {'compartment':compartment,'fileRefTitle':fileRefTitle,'fileRefNo':fileRefNo,'documentCount':documentCount,'caseRefs':caseRefs}
        filereferencelist.append(fl)
    return filereferencelist


@login_required
def index(request):

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    print ('storage:',storage)
    credential = storage.get()
    print ('credential:',credential)
    if credential is None:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()


        print ('authorize_url:',authorize_url)
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        print ('http:',http)
        http = credential.authorize(http)
        print ('http:',http)

        service = build("plus", "v1", http=http)
        print ('service:', service)
        activities = service.activities()
        activitylist = activities.list(collection='public',
                                   userId='me').execute()
        logging.info(activitylist)

        return render(request, 'welcome.html', {
                'activitylist': activitylist,
                })

    SCOPES = 'https://mail.google.com/,https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.metadata'
    store = file.Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        print ('flow:',flow)
        creds = tools.run_flow(flow, store)
    print('creds:',creds)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    profile = service.users().getProfile(userId='me').execute()
    print (profile['emailAddress'])

    inputarg = {
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


    response = service.users().watch(userId=profile['emailAddress'], body=inputarg).execute()
    print (response)


    previous_url = request.META.get('HTTP_REFERER')
    if previous_url is None: 
        previous_url =''
        print ("none")
    else:
        print (previous_url)

    page = request.GET.get('page',1)


    wsdl = 'http://mykris.sqlview.com:8080/KRIS/services/krislitews?wsdl'
    soapclient = zeep.Client(wsdl=wsdl,strict=False)
    logintoken = soapclient.service.login('fong','p@ssw0rd.1','web','web')
    list = soapclient.service.findAllFileRefsByPage('fong',page,"",1,"","")
    alllist = getlist(list)
    print (alllist)
    list = soapclient.service.findFavoriteFileRef('fong')
    favlist = getlist(list)
    list = soapclient.service.findLastAccessedFileRef('fong')
    lastaccesslist = getlist(list) 


    



    c = {'alllist':alllist, 'favlist':favlist, 'lastaccesslist':lastaccesslist}
    print (c)

    return render (request, 'filereferencelist.html', c)
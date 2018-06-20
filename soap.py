import zeep
wsdl = 'http://mykris.sqlview.com:8080/KRIS/services/krislitews?wsdl'
client = zeep.Client(wsdl=wsdl,strict=False)
logintoken = client.service.login('fong','p@ssw0rd.1','web','web')
list = client.service.findAllFileRefs('fong')
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
   # 	print (rowelement.tag,":",rowelement.text, "   ",)

    	if rowelement.tag == 'fileRefTitle':
    		fileRefTitle = rowelement.text
    	if rowelement.tag == 'documentCount':
    		documentCount = rowelement.text
    	if rowelement.tag == 'securityGrading':
    		securityGrading = rowelement.text
    	if rowelement.tag == 'fileRefNo':
    		fileRefNo = rowelement.text

    print('compartment:',compartment,'fileRefTitle:',fileRefTitle,'fileRefNo:',fileRefNo,'documentCount:',documentCount,'securityGrading:',securityGrading, 'caseRefs:',caseRefs)
	

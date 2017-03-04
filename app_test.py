#
# Intent of this code is to create HTTP requests to send over to the database
# API quickly.  I'm tiring of manually creating requests in POSTMAN.  I want
# a standard set of tests that I can send immediately every time I update
# code.  Also, this will serve as an artifact (proof) of our testing.
#
# Helpful page:
# http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
#
import requests
url = 'https://projectbgroup7dev-timbram.c9users.io'
port = 8080




#############################
request = 'bus_list'
#############################
req_string = url + ':' + str(port) + '/' + request
print('----------------------------------------------------------------')
print('REQUEST:')
print('    ' + req_string)
print('RESPONSE:')
response = requests.get(req_string)
print ('    ' + str(response))
print ('    ' + response.text)




#############################
request = 'bus_list_with_pass'
#############################
req_string = url + ':' + str(port) + '/' + request
print('----------------------------------------------------------------')
print('REQUEST:')
print('    ' + req_string)
print('RESPONSE:')
response = requests.get(req_string)
print ('    ' + str(response))
print ('    ' + response.text)
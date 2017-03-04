import requests
#
# Intent of this code is to create HTTP requests to send over to the database
# API quickly.  I'm tiring of manually creating requests in POSTMAN.  I want
# a standard set of tests that I can send immediately every time I update
# code.  Also, this will serve as an artifact (proof) of our testing.
#
# Helpful page:
# http://docs.python-requests.org/en/latest/user/quickstart/#more-complicated-post-requests
#

# NOTE
# use the next couple lines to change BASE URL or port number
# NOTE
url = 'https://projectbgroup7dev-timbram.c9users.io'
port = 8080

# NOTE
# function definitions for tests start here
# NOTE
def generic_get_request(request):
    req_string = url + ':' + str(port) + '/' + request
    print('----------------------------------------------------------------')
    print('REQUEST:')
    print('    ' + req_string)
    print('RESPONSE:')
    response = requests.get(req_string)
    print (response)
    response = response.json()
    for each_record in response:
        print(each_record)
    print('\r') #formatting only
    return;

def request_list_of_businesses():
    request = 'bus_list'
    generic_get_request(request)

def request_list_of_businesses_with_passwords():
    request = 'bus_list_with_pass'
    generic_get_request(request)

def register_business(name, addr, city, state, zip, username, password, confirm_password):
    request = 'bus_register'
    req_string = url + ':' + str(port) + '/' + request
    post_data = {'name': name,
        'addr': addr,
        'city': city,
        'state': state,
        'zip': zip,
        'username': username,
        'password': password,
        'confirm_password': confirm_password}
    print('----------------------------------------------------------------')
    print('REQUEST:')
    print('    ' + req_string)
    print('POST DATA:')
    print('    ' + str(post_data))
    print('RESPONSE:')
    response = requests.post(req_string, post_data)
    print ('    ' + str(response))
    print ('    ' + response.text)
    return;

# NOTE
# actual calls to function for tests start here
# NOTE
request_list_of_businesses()
request_list_of_businesses_with_passwords()

register_business('Cash\'s Bar', '12000 SE Petrovitsky Rd', 'Renton', 'WA', '98058', 'A-money', 'asdf1234', 'asdf1234')
register_business('Cash\'s Grill', '3040 118th Ave SE', 'Bellevue', 'WA', '98005', 'B-money', '56hjkl78', '56hjkl78')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', 'WA', '98109', 'C-money', 'qwerty9876', 'qwerty9876')
request_list_of_businesses()
request_list_of_businesses_with_passwords()

register_business('', '200 Roy Street', 'Seattle', 'WA', '98109', 'C-money', 'qwerty9876', 'qwerty9876')
register_business('Cash\'s Pub', '', 'Seattle', 'WA', '98109', 'C-money', 'qwerty9876', 'qwerty9876')
register_business('Cash\'s Pub', '200 Roy Street', '', 'WA', '98109', 'C-money', 'qwerty9876', 'qwerty9876')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', '', '98109', 'C-money', 'qwerty9876', 'qwerty9876')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', 'WA', '', 'C-money', 'qwerty9876', 'qwerty9876')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', 'WA', '98109', '', 'qwerty9876', 'qwerty9876')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', 'WA', '98109', 'C-money', '', 'qwerty9876')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', 'WA', '98109', 'C-money', 'qwerty9876', '')
register_business('Cash\'s Pub', '200 Roy Street', 'Seattle', 'WA', '98109', 'C-money', 'qwerty9876', 'mismatch')



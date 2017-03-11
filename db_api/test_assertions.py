import os
import unittest
import requests
import tempfile

url = 'https://projectbgroup7dev-timbram.c9users.io'
port = 8080

class TestStringMethods(unittest.TestCase):
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    #tests the POST 'bus_register' and the GET 'bus_list' route for success
    def test_add_business(self):
        #add the business
        response = self.register_business('Priscilla\'s Diner', '100 Lakes Rd', 'Springfield Lakes', 'WA', '43000', 'priscilla', 'password', 'password')
        self.assertEqual(response.status_code, 200)
        #check the business list to see the business is there
        response = self.generic_get_request('bus_list')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        a =   ["Priscilla's Diner", "100 Lakes Rd", "Springfield Lakes", "WA", "43000", "priscilla"]
        self.assertIn(a, response)

    #tests the POST 'ben_register' and the GET 'ben_list' route for success
    def test_add_beneficiary(self):
        #add the beneficiary
        response = self.register_beneficiary("George", "Martin", "5 The Long Road", "Newark", "NJ", "42535", 2, "george_martin", 'password', 'password')
        self.assertEqual(response.status_code, 200)
        #check the beneficiary list to see the beneficiary is there
        response = self.generic_get_request('ben_list')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        a = ["George", "Martin", "5 The Long Road", "Newark", "NJ", "42535", 2, "george_martin"]
        self.assertIn(a, response)

    def test_bus_list_with_pass(self):
        response = self.generic_get_request('bus_list_with_pass')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        for each_record in response:
            self.assertEqual(len(each_record), 8)

    def test_ben_list_with_pass(self):
        response = self.generic_get_request('ben_list_with_pass')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        for each_record in response:
            self.assertEqual(len(each_record), 10)

    def test_bus_list(self):
        response = self.generic_get_request('bus_list')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        for each_record in response:
            self.assertEqual(len(each_record), 6)

    def test_ben_list(self):
        response = self.generic_get_request('ben_list')
        self.assertEqual(response.status_code, 200)
        response = response.json()
        for each_record in response:
            self.assertEqual(len(each_record), 8)
            
    def test_food_loss_no_session(self):
        # no session, expecting a 400 response or higher
        response = self.generic_get_request('food_loss')
        self.assertGreaterEqual(response.status_code, 400)
        response = response.json()

    def generic_get_request(self, request):
        req_string = url + ':' + str(port) + '/' + request
        response = requests.get(req_string)
        return response;

    def register_business(self, name, addr, city, state, zip, username, password, confirm_password):
        request = 'bus_register'
        req_string = url + ':' + str(port) + '/' + request
        post_data = {
            'name': name,
            'addr': addr,
            'city': city,
            'state': state,
            'zip': zip,
            'username': username,
            'password': password,
            'confirm_password': confirm_password
        }
        return requests.post(req_string, post_data)
    
    def register_beneficiary(self, first, last, addr, city, state, zip, famsize, username, password, confirm_password):
        request = 'ben_register'
        req_string = url + ':' + str(port) + '/' + request
        post_data = {
            'first': first,
            'last': last,
            'addr': addr,
            'city': city,
            'state': state,
            'zip': zip,
            'famsize': famsize,
            'username': username,
            'password': password,
            'confirm_password': confirm_password
        }
        return requests.post(req_string, post_data)

if __name__ == '__main__':
    unittest.main()

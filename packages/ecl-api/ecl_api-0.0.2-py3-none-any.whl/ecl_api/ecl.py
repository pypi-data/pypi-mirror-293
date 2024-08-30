'''
Contains code to talk to the ECL API
'''
import uuid
import hashlib
import requests

class ECL:
    '''
    The main ECL class that handles the connection with the ECL
    '''

    #pylint: disable=invalid-name,too-many-arguments

    def __init__(self, url, user, password, timeout=60, debug=False):
        '''
        Contructor

        Args:
            url (str): the URL
            user (str): the username
            password (str): the password
            timeout (int): request timeout in seconds
        '''

        self._url = url
        self._password = password
        self._user = user

        self._to = timeout

        self._debug = debug


    def generate_salt(self):
        '''
        Generates the salt random string
        '''

        return 'salt=' + str(uuid.uuid4())

    def signature(self, arguments, data=''):
        '''
        Constructs the signature, which is made with the arguments to pass to
        the API, the password, and the data (is POST) separated by ":". And the
        encoded.
        '''

        string = arguments
        string += ':'
        string += self._password
        string += ':'
        string += data

        # print('Signature string:', string)

        m = hashlib.md5()
        m.update(string.encode('utf-8'))
        return m.hexdigest()


    def search(self, category='Purity+Monitors', limit=2):
        '''
        Searched the last entries in a given category

        Args:
            category (str): the category to search in
            limit (int): limit to the number of entries
        '''

        url = self._url
        url += '/xml_search?'

        arguments = f'c={category}&'
        arguments += f'l={limit}&'
        arguments += self.generate_salt()

        # headers = {'content-type': 'text/xml'}

        headers = {
            'X-Signature-Method': 'md5',
            'X-User': self._user,
            'X-Signature': self.signature(arguments)
        }

        r = requests.get(url + arguments, headers=headers, timeout=self._to)

        return r.text

    def get_entry(self, entry_id=2968):
        '''
        Gets a particular entry.

        Args:
            entry_id (int): The ID of the entry 
        '''

        url = self._url
        url += '/xml_get?'

        arguments = f'e={entry_id}&'
        arguments += self.generate_salt()

        headers = {
            'X-Signature-Method': 'md5',
            'X-User': self._user,
            'X-Signature': self.signature(arguments)
        }

        r = requests.get(url + arguments, headers=headers, timeout=self._to)

        return r.text


    def post(self, entry, do_post=False):
        '''
        Posts an entry to the e-log

        Args:
            entry (ECLEntry): the entry
            do_post (bool): set this to True to submit the entry to the ECL
        '''

        entry.set_author(self._user)

        xml_data = entry.show()

        url = self._url
        url += '/xml_post?'

        arguments = self.generate_salt()

        # headers = {'content-type': 'text/xml'}

        headers = {
            'content-type': 'text/xml',
            'X-Signature-Method': 'md5',
            'X-User': self._user,
            'X-Signature': self.signature(arguments, xml_data)
        }

        if self._debug:
            print('Headers:', headers)
            print('URL:', url + arguments)

        if do_post:
            r = requests.post(url + arguments, headers=headers, data=xml_data, timeout=self._to)

            if self._debug:
                print(r.url)
                print(r.text)

            print('Posted.')

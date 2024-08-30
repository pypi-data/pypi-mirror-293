# This Python script is the XHR API to perform the BIMA synchronization requests
# Created on 2024-05-13

from datetime import datetime as dt
from lxml import html
import csv
import datetime
import json
import math
import openpyxl as xl
import os
import platformdirs as pd
import requests
import tempfile as temp
import time

class WerkudaraAPI(object):
    
    # The following constants are used to create the user dir
    APP_NAME = 'werkudara'
    APP_AUTHOR = 'groaking'
    
    # The user dir
    # (not necessarily a constant. It is initialized upon class creation
    # and its value is never altered throughout the execution)
    USER_DIR = pd.user_data_dir(APP_NAME, APP_AUTHOR)
    
    # The JSON files stored in the user dir
    JSON_SETTINGS = USER_DIR + '/settings.json'
    
    # The CSV files stored in the user dir
    CSV_DATABASE = USER_DIR + '/database.csv'
    
    URL_GET_DATA = 'https://great-3lxzvwrcxq-et.a.run.app/api/v1/pt/dosen'
    URL_LOGIN = 'https://great-3lxzvwrcxq-et.a.run.app/api/v1/auth/login'
    URL_ORIGIN = 'https://bima.kemdikbud.go.id/login'
    URL_SYNC = 'https://great-3lxzvwrcxq-et.a.run.app/api/v1/dosen/pddikti/sync-by-nidn'
    
    def __init__(self):
        # Initializing the class
        # Abstracting important and versatile variables
        self.username = ''
        self.password = ''
        self.auth_token = ''
        
        # Abstracting the statistics and lecturers info list
        self.reset_all_lecturer_info()
        self.reset_stats()
        
        # Creating the Python requests object
        self.s = requests.Session()
        
        # Initializing the user config directory and parsing JSON files
        self.initialize_user_dir()

    def connect(self):
        '''
        Connect the specified user credentials with BIMA.
        Returns "True" if login was successful, "False" if otherwise.
        If the specified credentials are correct, also return
        the BIMA authorization token.
        
        The return object is a list with two elements.
        '''
        
        # Clearing the cookie
        self.s.cookies.clear()
        
        # Loading the origin page
        self.s.get(self.URL_ORIGIN)
        
        # Preparing the login data payload
        d = { 'username': self.username, 'password': self.password }
        
        # Connecting with the login handler page
        r = self.s.post(self.URL_LOGIN, data=d)
        c = r.content.decode('utf-8')
        j = json.loads(c)
        
        # Recounts the statistics
        self.enumerate_stats()
        
        # Checking if the login was successful
        if str(j['message']) == 'OK' and str(j['code']) == '200':
            # Save the auth token for other functions to access
            self.auth_token = str('Bearer ' + j['data'].strip())
            
            return [True, self.auth_token]
        else:
            return [False, '']
    
    def enumerate_stats(self):
        '''Recounts the statistics of the BIMA lecturers. 
        
        :return: True if the process ends without error, false if otherwise
        '''
        is_success = False
        
        # The statistics list, reset from zero
        self.reset_stats()
        s = self.stats
        
        # Opening the CSV file for parsing
        # SOURCE: https://docs.python.org/3/library/csv.html#examples
        with open(self.CSV_DATABASE, newline='') as f:
            reader = csv.reader(f, quotechar='"')
            try:
                for row in reader:
                    
                    # Counting key statistics values of active lecturers
                    if row[12].strip() == 'Aktif Mengajar':
                        s['active'] += 1
                        
                        # Surround with try-catch statement;
                        # If a column is not present in a lecturer's row, we skip it
                        # and continue to count the next possible value
                        try:
                            # If the current lecturer is active, also count
                            # other imporant statistics; using switch-case
                            # SOURCE: https://www.freecodecamp.org/news/python-switch-statement-switch-case-example/
                            match row[13].strip():
                                case 'S2':
                                    s['degree']['s2'] += 1
                                case 'S3':
                                    s['degree']['s3'] += 1
                        except IndexError:
                            pass
                        
                        try:
                            match row[1].strip():
                                case 'Asisten Ahli':
                                    s['role']['aa'] += 1
                                case 'Lektor':
                                    s['role']['l'] += 1
                                case 'Lektor Kepala':
                                    s['role']['lk'] += 1
                                case 'Profesor':
                                    s['role']['prof'] += 1
                        except IndexError:
                            pass
                        
                        try:
                            match row[9].strip():
                                case 'Laki-Laki':
                                    s['gender']['m'] += 1
                                case 'Perempuan':
                                    s['gender']['f'] += 1
                        except IndexError:
                            pass
                            
                is_success = True
                
            except csv.Error as e:
                self.l(f'Error encountered in CSV parsing: {e}')
                is_success = False
            
            # Assign the statistics list into the object's variable, then return success
            self.stats = s
            return is_success
    
    def enumerate_all_lecturer_info(self):
        '''
        Enumerate all lecturers detailed info so that those info
        can be processed by the GUI.
        
        :return: True if the process ends without error, false if otherwise
        '''
        is_success = False
        
        # The enumerated info list, reset from "Empty List"
        self.reset_all_lecturer_info()
        
        # Opening the CSV file for parsing
        # SOURCE: https://docs.python.org/3/library/csv.html#examples
        with open(self.CSV_DATABASE, newline='') as f:
            reader = csv.reader(f, quotechar='"')
            try:
                # Skip header row by assigning "[1:]"
                for row in [a for a in reader][1:]:
                    # Skip non-active lecturers
                    if row[12].strip() != 'Aktif Mengajar':
                        continue
                    
                    # Create new dict
                    b = {}
                    
                    # Writing data into the empty dict
                    b['name'] = row[0]
                    b['role'] = row[1]
                    b['program'] = row[2]
                    b['nidn'] = row[3]
                    b['nat_id'] = row[4]
                    b['birthplace'] = row[5]
                    b['dob'] = row[6]
                    b['phone'] = row[7]
                    b['email'] = row[8]
                    b['gender'] = row[9]
                    b['affiliation'] = row[10]
                    b['address'] = row[11]
                    b['highest_degree'] = row[13]
                    
                    # Appending this lecturer's specific dict into the global list
                    self.all_lecturer_info.append(b)
                
                # If we can get into this line without error, the code completes successfully
                is_success = True
                
            except csv.Error as e:
                self.l(f'Error encountered in CSV parsing: {e}')
                is_success = False
            
            # Closing the file input stream
            f.close()
            
            # Assign the statistics list into the object's variable, then return success
            return is_success
    
    def get_all_lecturer_info(self):
        ''' Returns an enumerated and column-transposed list of lecturers. '''
        self.enumerate_all_lecturer_info()
        return self.all_lecturer_info
    
    def get_stats(self):
        '''
        Returns a list of lecturer-related information
        which will be displayed as a statistics at the
        first tab of the app
        '''
        self.enumerate_stats()
        return self.stats
    
    def initialize_user_dir(self):
        '''
        Ensures that the user config directory is present
        and the settings-and-data JSON files are valid
        '''
        
        # Ensuring that the user directory exists
        try:
            os.mkdir(self.USER_DIR)
            self.l(f'User config folder created: {self.USER_DIR}')
        except FileExistsError:
            self.l(f'User config folder already exists: {self.USER_DIR}')
        
        # Checking if the settings JSON file exists and is valid
        try:
            with open(self.JSON_SETTINGS, 'r') as a:
                s = ''
                for l in a:
                    s += l + '\n'
                s = s.strip()
                a.close()
                
                # Assigning the parsed JSON values into a Python dictionary
                self.settings = json.loads(s)

        except:
            # If the JSON file does not exist
            # or if the JSON file is invalid
            # instead just recreate the JSON file from scratch
            with open(self.JSON_SETTINGS, 'w') as a:
                self.l('Settings JSON error detected! Creating settings.json from scratch ...')
                a.close()
            
            # Then, create an empty JSON framework
            # (forget the single quotes; they will be converted
            # to double-quote upon JSON dumping)
            # ---
            # The following dict is the default settings and configuration of the app
            self.settings = {
                # Saved credentials
                'remember_me': 0,
                'cred_user_hashed': '#',
                'cred_pass_hashed': '#',
                
                # Related to the API request to obtain BIMA Lecturer data
                'bima_apireq_datapresumption': 1000,  # --- How many lecturers are presumed in the current institution's database
                'bima_apireq_epr': 50,  # --- entries per request (EPR)
                
                # Related to the synchronization process
                'sync_max_tries': 10,  # --- how many tries before concluding "417" http code as "cannot sync"
            }
            
            self.update_settings()
    
    def l(self, message):
        ''' Back-end debug logger for the API class, never shown anywhere in the GUI '''
        print('::: [' + str(dt.now()) + '] + [API] ' + str(message))
    
    def purge(self):
        ''' Purge (remove and clean up) all local lecturers database. '''
        # Removing the database content
        with open(self.CSV_DATABASE, 'w') as f:
            f.close()
        
        # Purging and updating the statistics
        self.reset_stats()
        
        # Redundantly returns successful purgings
        return True
    
    def refresh(self, stats_update):
        '''Retrieve online data from BIMA and update the database.
        
        :param stats_update: The function from the main GUI which updates the statistics display.
        '''
        
        # Calculate the number of pages to request to the BIMA API
        # based on the configuration of EPR and presumed number of lecturers
        p = math.ceil( self.settings['bima_apireq_datapresumption'] / self.settings['bima_apireq_epr'] )
        
        # Reseting the CSV database
        with open(self.CSV_DATABASE, 'w') as a:
            a.close()
        
        # Preparing the CSV header and data body
        csv_header = 'name,role,program,nidn,nat_id,birthplace,dob,phone,email,gender,affiliation,address,is_active,highest_degree\n'
        csv_data = ''
        
        for i in range (1, p + 1):
            self.l(f'Requesting BIMA API data (Page {i}/{p}) ...')
            
            # First, we update the stats display
            stats_update()
            
            # Assembling the URL parameter
            url = f'{ self.URL_GET_DATA }?limit={ self.settings["bima_apireq_epr"] }&choose=nama&page={ str(i) }'
            
            # Assembling the request header
            h = { 'Authorization': self.auth_token }
            
            # Request the dosen data
            r = self.s.get(url, headers=h)
            c = r.content.decode('utf-8')
            j = json.loads(c)
            
            # Check if the response is not "OK"
            response_code = str(j['code'])
            if response_code != '200':
                self.l(f'Retrieved response code {response_code}. Page {i} cannot be loaded! Skipping ...')
                continue
            
            # Check if the data is null
            if j['data'] == None:
                self.l(f'Data from page {i} is empty! Skipping ...')
                continue
            
            # Iterate through every retrieved entry
            # (Given 200 response code and non-empty JSON data)
            for a in j['data']:
                
                # Check if the lecturer 'active' data is present
                if a['Additional']['is_active'].strip() == '':
                    continue
                
                # Obtaining the rest of column data
                # and align them all into suitable table columns
                d = [
                    a['Additional']['full_name'],
                    a['DosenIdentitas']['jabatan_fungsional']['jabatan'],
                    a['DosenIdentitas']['program_studi']['nama'],
                    a['Additional']['nidn'],
                    a['DosenIdentitas']['nomor_ktp'],
                    a['DosenIdentitas']['tempat_lahir'],
                    a['DosenIdentitas']['tanggal_lahir'],
                    a['DosenIdentitas']['nomor_telepon'],
                    a['DosenIdentitas']['surel'],
                    a['DosenIdentitas']['kode_jenis_kelamin'],
                    a['DosenIdentitas']['institusi']['nama'],
                    a['DosenIdentitas']['alamat'],
                    a['Additional']['is_active'],
                ]
                
                # Not every entry has "highest educational background" column
                try:
                    d.append( a['DosenIdentitas']['jenjang_pendidikan_tertinggi']['nama'].replace('\\n', '').strip() )
                except KeyError:
                    d.append('')
                
                # Removing new line characters (dangerous to CSV file structure!) from the arranged data
                # Also removing trailing and leading blank spaces
                e = [ ' '.join(l.splitlines()).replace('  ', ' ').strip() for l in d ]
                d = e.copy()
                
                # Writing into the CSV body
                s = ''
                for l in d:
                    s += f'"{l}",'
                csv_data += s[:-1] + '\n'
            
            # Truncate trailing and leading spaces in the csv data
            csv_data = csv_data.strip()
            
            # Writing the CSV database file
            with open(self.CSV_DATABASE, 'w') as a:
                self.l(f'Writing {str(len(csv_data.split("\n")))} entries into the CSV database ...')
                a.write( (csv_header + csv_data) )
                a.close()
        
        # Recound the statistics on the main page/tab
        self.enumerate_stats()
        
        return True
    
    def reset_all_lecturer_info(self):
        ''' Resets the "All lecturers list" info "Empty list". '''
        self.all_lecturer_info = []
    
    def reset_stats(self):
        ''' Resets the stats count to zero. '''
        # The statistics list, reset from zero
        self.stats = {
            'active': 0,
            'degree': {
                's2': 0,
                's3': 0,
            },
            'role': {
                'aa': 0,
                'l': 0,
                'lk': 0,
                'prof': 0,
            },
            'gender': {
                'm': 0,
                'f': 0,
            },
        }
    
    def set_credentials(self, user_, pass_):
        ''' Altering the BIMA operator login credential '''
        self.username = user_
        self.password = pass_
    
    def sync(self, sync_list, o, p):
        ''' This object executes the synchronization process of BIMA lecturers.
        
        :param sync_list: The list of lecturers (along with their detailed information)
                          that this method/function will sync.
        :param o: The main GUI's message output writer.
        :param p: The main GUI's progress bar changer method.
        :return: True if the sync was successful, False if an error (any error) was returned.
        '''
            
        # Reset the previous progress bar value
        p(0)
        
        # Obtaining the length of the sync_list
        x = len(sync_list)
        
        # Setting the global request header
        headers = { 'Authorization': self.auth_token }
        
        # Loading the origin page
        self.s.get(self.URL_ORIGIN)
        
        # Counting the statistics of failed vs successful sync attempts
        stats_successful = 0
        stats_failed = 0
        
        h = -1
        for a in sync_list:
            # Get NIDN and name info
            nidn = a['nidn']
            name = a['name']
            
            # Determining the ordinal of the current lecturer's sync queue
            h += 1
            
            # Reporting to the user about what is currently being done
            o(f'Synchronizing {name} in progress ...', True)
        
            # Check if 'nidn' is nonempty
            if nidn == '':
                o(f'Lecturer {name} does not have NIDN. Skipping ...', False)
                stats_failed += 1
                continue
        
            # Modifying the URL according to the NIDN data
            url_sync = self.URL_SYNC + '/' + nidn
            
            # As long as 'max_attempt' is not reached,
            # continue attempting to sync author whenever "417" code is returned
            max_attempt = self.settings['sync_max_tries']
            for i in range(max_attempt + 1):
                
                # Begin requesting "PUT" request for the sync of the dosen
                try:
                    o('Sending the http "PUT" request ...', False)
                    r = self.s.put(url_sync, data='', headers=headers)
                    c = r.content.decode('utf-8')
                except:
                    # Some error was detected (usually connection reset) and the sync process was disturbed
                    o('Some unknown error was detected! Please check your internet connection.', True)
                    return False
                
                # Check if 500 internal server error is encountered,
                # which returns "runtime error: invalid memory address or nil pointer dereference"
                if c.__contains__('runtime error: invalid memory address or nil pointer dereference'):
                    # Just give up
                    if i == max_attempt:
                        stats_failed += 1
                        o(f'Syncing {name} -- invalid memory address or nil pointer dereference. Max attempt count is reached. Skipping ...', False)
                        break
                    else:
                        o(f'Syncing {name} -- invalid memory address or nil pointer dereference. Retrying [ATTEMPT {i}] ...', False)
                        continue
                    
                j = json.loads(c)
            
                # Interpreting the server API's response
                response_code = j['code']
                response_message = j['message']
                
                # Logging the sync result
                o(f'+ Syncing {name} -- STATUS: {response_code} {response_message}', False)
            
                # If successful, horray!
                if str(response_code) == str(200):
                    o(f'Success!', False)
                    stats_successful += 1
                    break
                else:
                    # Just give up
                    if i == max_attempt:
                        stats_failed += 1
                        o(f'+ Cannot sync: {name}! Max attempt count is reached. Skipping ...', False)
                        break
                    else:
                        o(f'+ Cannot sync: {name}! Retrying to sync the data [ATTEMPT { i+1 }/{max_attempt}] ...', False)
                        continue
            
            # Deal with the progress bar progression
            cur = round( ((h + 1)/x) * 100 )
            p(cur)
            
        return True
    
    def update_settings(self):
        ''' Writing the app's temporary settings dict into an external JSON file '''
        with open(self.JSON_SETTINGS, 'w') as a:
            self.l('Exporting settings right now ...')
            a.write(json.dumps(self.settings))
            a.close()
    

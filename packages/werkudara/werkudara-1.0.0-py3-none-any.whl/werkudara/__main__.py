# This file is executed first for the AutoSINTA GUI application
# Created on 2024-05-13

# REFERENCES:
#  [1] Viewing the UI script created using QtDesigner:
#    -> https://www.pythonguis.com/tutorials/first-steps-qt-creator/
#  [2] PyQt5 event listener:
#    -> https://www.techwithtim.net/tutorials/pyqt5-tutorial/buttons-and-events
#  [3] KActionSelector is cumbersome:
#    -> https://stackoverflow.com/questions/12591456
#  [4] You need to execute 'self.exec_()' to show a QDialog:
#    -> https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QDialog.html#code-examples
#  [5] QLineEdit API documentation:
#    -> https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QLineEdit.html
#  [6] QPlainTextEdit API documentation:
#    -> https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPlainTextEdit.html
#  [7] GUI freezing? Use "QtCore.QCoreApplication.processEvents()":
#    -> https://www.xingyulei.com/post/qt-threading/index.html
#  [8] Pivotting a dict into a list
#    -> https://stackoverflow.com/a/37489445
#  [9] Sorting a list of dicts by a certain key
#    -> https://stackoverflow.com/a/73050
# [10] To move an item from a QListWidget, clone it!
#    -> https://stackoverflow.com/a/68229287
# [11] Listing the list of items in a QListWidget
#    -> https://stackoverflow.com/a/22572524
# [12] Base64 Encode/Decode
#    -> https://www.geeksforgeeks.org/python-strings-decode-method

# Enable tracing of bugs in case of application crashes
# SOURCE: https://stackoverflow.com/a/60414546
import faulthandler
faulthandler.enable()

# Importing essential Python modules
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from datetime import datetime as dt
from queue import Queue
import base64
import os
import sys
import tarfile
import time

# Importing the UI python scripts
from ui_exported import main_gui
from ui_exported import universal_dialog

# Importing the application's API
import api

# Importing the multithreading wiht result library
from thread import ThreadWithResult

class DialogUniversal(QtWidgets.QDialog, universal_dialog.Ui_Dialog):
    def __init__(self, *args, obj=None, **kwargs):
        super(DialogUniversal, self).__init__(*args, **kwargs)
        self.setupUi(self)
    
    def display(self, s_title, s_message):
        '''
        Display this dialog window with a given window title and message
        as specified in the function's argument.
        Then directly show the dialog window.
        '''
        self.set_content(s_title, s_message)
        self.exec()
    
    def set_content(self, s_title, s_message):
        '''
        Setting the message to be displayed in the dialog, as well as
        the window title of the dialog.
        '''
        self.label_message.setText(s_message)
        self.setWindowTitle(s_title)

class WindowMain(QtWidgets.QMainWindow, main_gui.Ui_MainWindow):
    '''
    Werkudara API is solely controlled and accessed in this class.
    This class controls the main GUI as well as the sync operations.
    '''
    
    # Custom signals for the function's logger and progresser
    # (Qt GUI should not be altered outside the MainWindow directly)
    # SOURCE: https://stackoverflow.com/a/21863366
    log = QtCore.pyqtSignal(str, bool)
    progress = QtCore.pyqtSignal(int)
    
    # ------------------___-------------------------------------_ #
    
    def __init__(self, *args, obj=None, **kwargs):
        super(WindowMain, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.o('Loading graphical user interface ...')
        
        # Creating custom signal/slot so that outside classes can access
        # this GUI's "o()" and "p()" functions
        # SOURCE: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html
        self.log.connect(self.o)
        self.progress.connect(self.p)
        
        # Set event listener
        self.btn_export.clicked.connect(self.btn_export_clicked)
        self.btn_import.clicked.connect(self.btn_import_clicked)
        self.btn_login.clicked.connect(self.btn_login_clicked)
        self.btn_move_left.clicked.connect(self.btn_move_left_clicked)
        self.btn_move_right.clicked.connect(self.btn_move_right_clicked)
        self.btn_purge.clicked.connect(self.btn_purge_clicked)
        self.btn_refresh.clicked.connect(self.btn_refresh_clicked)
        self.btn_sync_now.clicked.connect(self.btn_sync_now_clicked)
        self.checkbox_remember.clicked.connect(self.checkbox_remember_clicked)
        self.frame_tab.currentChanged.connect(self.frame_tab_selected)
        self.list_active_lecturers.itemSelectionChanged.connect(self.list_active_lecturers_change)
        self.radio_sync_all.clicked.connect(self.radio_sync_all_clicked)
        self.radio_sync_some.clicked.connect(self.radio_sync_some_clicked)
        
        # Initializing the API
        self.o('Initializing the Werkudara API ...')
        self.api = api.WerkudaraAPI()
        
        # Initializing the credential input
        # (Did the user store last login information?)
        if self.api.settings['remember_me'] == 1:
            # Decoding stored credential information
            u_dec = base64.b64decode(self.api.settings['cred_user_hashed']).decode('utf-8')
            p_dec = base64.b64decode(self.api.settings['cred_pass_hashed']).decode('utf-8')
            
            # Autofilling the form
            self.input_user.setText(u_dec)
            self.input_pass.setText(p_dec)
            self.checkbox_remember.setChecked(True)
    
    def btn_export_clicked(self):
        # Attempting to export all local lecturers data
        self.o(f'Exporting the lecturers database ...')
        
        # Asking for file export path ("ff" = "file filter")
        reference_filename = f'Werkudara Database Backup { str(dt.now()).split(".")[0].replace(":", "-").replace(" ", "-") }.tar.xz'
        ff = "XZ-compressed Tar archive (*.tar.xz)"
        out = QtWidgets.QFileDialog.getSaveFileName(self, 'Export BIMA lecturers database to ...', reference_filename, ff)
        out = out[0]
        
        # Mitigate user cancel
        if out == '':
            self.o(f'Export cancelled!')
            return
        
        # Ensures that the filename ends in ".tar.xz"
        if str.lower(out)[-7:] != '.tar.xz':
            out += '.tar.xz'
        
        # Change to the database's directory
        old_wd = os.getcwd()
        os.chdir(self.api.USER_DIR)
        
        # Perform database compression
        self.o(f'Exporting database to {out} ...')
        tar = tarfile.open(name=out, mode='w:xz')
        tar.add('database.csv', recursive=False)
        tar.close()
        
        # Moving back to the previous working directory
        os.chdir(old_wd)
        
        # Successful logging
        DialogUniversal().display('Export successful!', f'All of BIMA lecturers data have been exported to {out} successfully!')
    
    def btn_import_clicked(self):
        # Attempting to import all local lecturers data
        self.o(f'Importing the lecturers database ...')
        
        # Asking for the file path to be imported ("ff" = "file filter")
        ff = "XZ-compressed Tar archive (*.tar.xz)"
        imp = QtWidgets.QFileDialog.getOpenFileName(self, 'Import BIMA database from ...', '', ff)
        imp = imp[0]
        
        # Mitigate user cancel
        if imp == '':
            self.o(f'Database import cancelled!')
            return
        
        # Check if the selected file is an XZ-compressed Tar archive
        if tarfile.is_tarfile(imp):
            tar = tarfile.open(name=imp, mode='r:xz')
            tar.extract('database.csv', self.api.USER_DIR)
            tar.close()
            
            # Update statistics display
            self.update_stats_display()
            
            # Successful logging
            DialogUniversal().display('Import successful!', f'The selected BIMA database archive has been imported into the application successfully, overwriting any previous data.')
            return
        
        # Failed logging
        DialogUniversal().display('Import error', f'The selected file is not a valid XZ-compressed Tar archive: {imp}')
    
    def btn_login_clicked(self):
        # Obtaining and setting the login credentials
        u = self.input_user.text()
        p = self.input_pass.text()
        self.api.set_credentials(u, p)
        
        # Encoding the credentials in base64 format
        u_crypt = base64.b64encode(u.encode('utf-8')).decode('utf-8')
        p_crypt = base64.b64encode(p.encode('utf-8')).decode('utf-8')
        
        # Attempting to do the login
        self.o(f'Attempting to login user [{u}] ...')
        
        # Disable essential buttons during the login process
        self.essential_buttons_disable()
        
        # Using multithreading to prevent GUI freezing
        # SOURCE: https://stackoverflow.com/a/65447493
        t = ThreadWithResult(target=self.api.connect)
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                r = t.result
                t.join()
                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()
        
        # Determining the actions to take upon receiving the responses
        if r[0] == True:
            self.o(f'Login successful!')
            DialogUniversal().display('Login successful!', 'Login to BIMA successful! You may proceed with the synchronization operations.')
            
            # Re-enable functional components
            self.frame_log.setEnabled(True)
            self.frame_tab.setEnabled(True)
            self.list_active_lecturers.setEnabled(True)
            
            # Update statistics according to the logged-in account's affiliation
            self.update_stats_display()
        else:
            self.o(f'Login failed!')
            DialogUniversal().display('Login failed!', 'Cannot login to BIMA with the specified credentials. Please make sure that the username and password you entered are correct.')
        
        # Determining whether we should keep the login credential information
        if self.checkbox_remember.isChecked():
            self.api.settings['remember_me'] = 1
            self.api.settings['cred_user_hashed'] = u_crypt
            self.api.settings['cred_pass_hashed'] = p_crypt
        else:
            self.api.settings['remember_me'] = 0
            self.api.settings['cred_user_hashed'] = '#'
            self.api.settings['cred_pass_hashed'] = '#'
        
        # At last, save the settings into the JSON file
        self.api.update_settings()
        
        # Re-enable essential buttons
        self.essential_buttons_enable()
    
    def btn_move_left_clicked(self):
        # Moving items selected from the right list to the left list
        for a in self.list_lecturers_right.selectedItems():
            # Clone the selected item, then move it to the other list
            b = a.clone()
            self.list_lecturers_left.addItem(b)
            
            # Get the index of the selected item, then remove the item from the list
            i = self.list_lecturers_right.indexFromItem(a).row()
            self.list_lecturers_right.takeItem(i)
        
        # Finally, sort the destination QListWidget
        self.list_lecturers_left.sortItems(Qt.AscendingOrder)
    
    def btn_move_right_clicked(self):
        # Moving items selected from the left list to the right list
        for a in self.list_lecturers_left.selectedItems():
            # Clone the selected item, then move it to the other list
            b = a.clone()
            self.list_lecturers_right.addItem(b)
            
            # Get the index of the selected item, then remove the item from the list
            i = self.list_lecturers_left.indexFromItem(a).row()
            self.list_lecturers_left.takeItem(i)
        
        # Finally, sort the destination QListWidget
        self.list_lecturers_right.sortItems(Qt.AscendingOrder)
    
    def btn_purge_clicked(self):
        # Attempting to remove all local lecturers database
        self.o(f'Purging the lecturers database ...')
        
        # Confirming if the user really wants to proceed
        # SOURCE: https://stackoverflow.com/questions/34253350
        qm = QtWidgets.QMessageBox
        ret = qm.question(self, 'Purging the Database', 'Are you sure to reset all of local statistics and database? You can always re-download and refresh the data from the server afterwards.', qm.Yes | qm.No)
        if ret == qm.No:
            self.o(f'Purging database cancelled!')
            return
        
        # Using multithreading to prevent GUI freezing
        # SOURCE: https://stackoverflow.com/a/65447493
        t = ThreadWithResult(target=self.api.purge)
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                r = t.result
                t.join()
                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()
        
        # Determining the actions to take upon receiving the responses
        if r == True:
            self.update_stats_display()
            DialogUniversal().display('Purging successful!', 'The Werkudara local database has been cleaned up.')
    
    def btn_refresh_clicked(self):
        # Attempting to do the refresh
        self.o(f'Refreshing database ...')
        
        # Disable all essential buttons during the refresh process
        self.essential_buttons_disable()
        
        # Using multithreading to prevent GUI freezing
        # SOURCE: https://stackoverflow.com/a/65447493
        t = ThreadWithResult(target=self.api.refresh, args=(self.update_stats_display,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                r = t.result
                t.join()
                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()
        
        # Determining the actions to take upon receiving the responses
        if r == True:
            self.update_stats_display()
            DialogUniversal().display('Refresh successful!', 'The Werkudara local database has been updated and synchronized with the server.')
        
        # Re-enable essential buttons
        self.essential_buttons_enable()
    
    def btn_sync_now_clicked(self):
        # Obtaining the list of all BIMA lecturers
        a = self.api.get_all_lecturer_info()
        
        # Read the option the user selected
        o = self.radio_sync_all.isChecked()
        
        # Mitigating user selections
        sync_list = []
        if o:  # --- sync all lecturers
            sync_list = a
        else:  # --- sync only selected lecturers
            sync_list = []
            
            # Listing the list of items in the right QListWidget
            # SOURCE: https://stackoverflow.com/a/22572524
            items = []
            for x in range( self.list_lecturers_right.count() ):
                items.append( self.list_lecturers_right.item(x) )
            
            # Sync some lecturers per user's selection
            # First we read the user's selection from the right list widget
            for b in items:
                
                # Read the back-end information about the item's index
                i = int( b.toolTip().split('INDEX:')[1].strip() )
                
                # Appending the current selection's item into the sync list
                sync_list.append(a[i])
        
        # Calculating the number of lecturers to sync
        _len = len(sync_list)
        self.o(f'Syncing {_len} BIMA lecturers now ...')
        
        # Disables all essential buttons during the sync process
        self.essential_buttons_disable()
        
        # Using multithreading to prevent GUI freezing
        # SOURCE: https://stackoverflow.com/a/65447493
        t = ThreadWithResult(target=self.api.sync, args=(sync_list, self.log.emit, self.progress.emit,))
        t.start()
        while True:
            if getattr(t, 'result', None):
                # Obtaining the thread function's result
                r = t.result
                t.join()
                break
            else:
                # When this block is reached, it means the function has not returned any value
                # While we wait for the thread response to be returned, let us prevent
                # Qt5 GUI freezing by repeatedly executing the following line:
                QtCore.QCoreApplication.processEvents()
        
        # Determining the actions to take upon receiving the responses
        if r == True:
            self.o('Synchronization complete and successful.')
            DialogUniversal().display('Sync Success', f'Synchronization complete! All {_len} BIMA lecturers data are now up-to-date.')
        else:
            self.o('Cannot continue syncing. Please check your internet connection.')
            DialogUniversal().display('Sync Failed', 'Synchronization failed! You may need to check your internet connection. Try again.')
        
        # Re-enable all essential buttons
        self.essential_buttons_enable()
        
    def checkbox_remember_clicked(self):
        # Obtaining and setting the login credentials
        u = self.input_user.text()
        p = self.input_pass.text()
        
        # Encoding the credentials in base64 format
        u_crypt = base64.b64encode(u.encode('utf-8')).decode('utf-8')
        p_crypt = base64.b64encode(p.encode('utf-8')).decode('utf-8')
        
        # Determining whether we should keep the login credential information
        if self.checkbox_remember.isChecked():
            self.api.settings['remember_me'] = 1
            self.api.settings['cred_user_hashed'] = u_crypt
            self.api.settings['cred_pass_hashed'] = p_crypt
        else:
            self.api.settings['remember_me'] = 0
            self.api.settings['cred_user_hashed'] = '#'
            self.api.settings['cred_pass_hashed'] = '#'
        
        # At last, save the settings into the JSON file
        self.api.update_settings()
    
    def essential_buttons_disable(self):
        '''Disables essential buttons from being clicked.
        
        The following is the list of buttons disabled upon calling this function:
        - Login button
        - Refresh button
        - Import local data button
        - Export database button
        - Purge all data button
        - Sync now button
        '''
        self.btn_login.setEnabled(False)
        self.btn_refresh.setEnabled(False)
        self.btn_import.setEnabled(False)
        self.btn_export.setEnabled(False)
        self.btn_purge.setEnabled(False)
        
        # Not buttons, but still need to be disabled during important processes
        self.btn_sync_now.setEnabled(False)
        self.checkbox_remember.setEnabled(False)
        self.input_pass.setEnabled(False)
        self.input_user.setEnabled(False)
    
    def essential_buttons_enable(self):
        '''Enables essential buttons in the main GUI
        
        The following is the list of buttons enabled upon calling this function:
        - Login button
        - Refresh button
        - Import local data button
        - Export database button
        - Purge all data button
        - Sync now button
        '''
        self.btn_login.setEnabled(True)
        self.btn_refresh.setEnabled(True)
        self.btn_import.setEnabled(True)
        self.btn_export.setEnabled(True)
        self.btn_purge.setEnabled(True)
        self.btn_sync_now.setEnabled(True)
        
        # Not buttons, but still need to be disabled during important processes
        self.checkbox_remember.setEnabled(True)
        self.input_pass.setEnabled(True)
        self.input_user.setEnabled(True)
    
    def frame_tab_selected(self):
        '''This function controls what to do when a tab is selected in "frame_tab"
        '''
        selected_tab = self.frame_tab.currentIndex()
        
        # Redundant logging
        self.o(f'Selected menu tab: {selected_tab}', False)
        
        if selected_tab == 0:
            pass
        elif selected_tab == 1:
            self.update_lecturer_list('sync')
        elif selected_tab == 2:
            self.update_lecturer_list('info')
    
    def list_active_lecturers_change(self):
        ''' The control function which determines actions to take upon
        list item change in the QListWidget "list_active_lecturers". '''
        
        # The selected item object
        obj = self.list_active_lecturers.selectedItems()
        
        if len(obj) == 0:
            # Nothing is selected. Why bother?
            self.o('There is no Easter Egg here. Go away!', False)
            return
        
        # Read the back-end information about the selected item's original data index
        i = int( obj[0].toolTip().split('INDEX:')[1].strip() )
        
        # Update the specified lecturer's detailed info
        self.update_lecturer_info(i)
    
    def o(self, str_: str, echo_user=True):
        '''
        "o" stands for "output message logging"
        Any string passed to the parameter "str_" will be logged to both
        the terminal and the application's message TextArea
        
        :param echo_user: Determines if the user should be notified by
                          echoing the log message into "area_message"
                          (defaults to "True")
        '''
        
        # Do the message logging
        if echo_user:
            print('::: [' + str(dt.now()) + '] + ' + str_)
            self.area_message.appendPlainText(str_)
        else:
            print('::: [' + str(dt.now()) + '] + [DEV] ' + str_)
            
        # Prevent freezing
        QtCore.QCoreApplication.processEvents()
    
    def p(self, int_: int):
        '''
        "p" stands for "progress bar"
        This function controls the value of the app's main progress bar.
        Useful during the synchronization process.
        '''
        
        # Filter the input values
        if int_ > 100:
            int_ = 100
        elif int_ < 0:
            int_ = 0
        int_ = int(int_)  # --- redundant, but nevermind.
        
        # Update the progress bar's value
        self.progress_sync.setProperty('value', int_)
        
        # Prevent freezing
        QtCore.QCoreApplication.processEvents()
    
    def radio_sync_all_clicked(self):
        ''' Determine what to do when "sync all" radio button is clicked. '''
        self.frame_lecturers.setEnabled(False)
        self.list_lecturers_left.setEnabled(False)
        self.list_lecturers_right.setEnabled(False)
    
    def radio_sync_some_clicked(self):
        ''' Determine what to do when "sync selected/some" radio button is clicked. '''
        self.frame_lecturers.setEnabled(True)
        self.list_lecturers_left.setEnabled(True)
        self.list_lecturers_right.setEnabled(True)
    
    def update_lecturer_info(self, idx):
        ''' Update a specific lecturer's info page in tab no. 3 ("info").
        
        :param idx: The lecturer's back-end index in the API's "all_lecturer_info" variable.
        '''
        # Get the selected lecturer's detailed info
        a = self.api.get_all_lecturer_info()[idx]
        
        # Assign each info data info its respective label
        self.info_name.setText(a['name'])
        self.info_role.setText(a['role'])
        self.info_program.setText(a['program'])
        self.info_nidn.setText(a['nidn'])
        self.info_nat_id.setText(a['nat_id'])
        self.info_birthplace.setText(a['birthplace'])
        self.info_dob.setText(a['dob'].split('T')[0])
        self.info_phone.setText(a['phone'])
        self.info_email.setText(a['email'])
        self.info_gender.setText(a['gender'])
        self.info_affiliation.setText(a['affiliation'])
        self.info_address.setText(a['address'])
        self.info_highest_degree.setText(a['highest_degree'])
        
        # Prevent freezing
        QtCore.QCoreApplication.processEvents()
    
    def update_lecturer_list(self, ttu):
        ''' Update the list of active lecturers in tab no. 2 ("sync") and tab no. 3 ("info").
        
        :param ttu: ("tab to update") determines which tab's lecturers list to update
                    possible values: ["sync", "info"]
        '''
        
        # Clearing any existing items from the QListWidget
        self.list_active_lecturers.clear()
        self.list_lecturers_left.clear()
        
        # Retrieving all lecturers detailed info
        a = self.api.get_all_lecturer_info()
        
        # Retrieving the original index of each data point
        # done before alphabetical sorting of lecturer changes the list's order
        i = 0
        for j in range(len(a)):
            a[j]['index'] = i
            i += 1
        
        # Sorting the SINTA author data by the lecturer name's alphabetical order
        # SOURCE: https://stackoverflow.com/a/73050
        b = sorted(a, key=lambda z: z['name'])
        
        # Enlisting the lecturers data into the QListWidget element
        for c in b:
            # Creating a new list item of QListWidgetItem type
            item = QtWidgets.QListWidgetItem(c['name'])
            
            # Creating a tooltip text, carrying back-end information
            tooltip_text = f'NIDN: { c["nidn"] }, INDEX: { c["index"] }'
            item.setToolTip(tooltip_text)
            
            # Appending to the QListWidget element
            if ttu == 'info':
                self.list_active_lecturers.addItem(item)
            elif ttu == 'sync':
                self.list_lecturers_left.addItem(item)
                # Preventing duplication when an item is already moved
                # to the "list_lecturers_right" QListWidget
                for i in range(self.list_lecturers_right.count()):
                    if tooltip_text.strip() == self.list_lecturers_right.item(i).toolTip():
                        j = self.list_lecturers_left.row(item)
                        self.list_lecturers_left.takeItem(j)
            else:
                self.o('Cannot append QListWidget element/item. Did you forget to specify tab name?', False)
        
        # Prevent freezing
        QtCore.QCoreApplication.processEvents()
    
    def update_stats_display(self):
        '''
        Update the values and display of lecturers' statistics
        in tab no. 1 ("homepage")
        '''
        
        # Recount the calculation of stats data
        self.api.enumerate_stats()
        
        # Obtaining the calculation of stats data
        d = self.api.get_stats()
        
        # Updating individual statistics placeholder
        self.stat_1.setText( str( d['active'] ))
        self.stat_2.setText( str( d['degree']['s2'] ))
        self.stat_3.setText( str( d['degree']['s3'] ))
        self.stat_4.setText( str( d['role']['aa'] ))
        self.stat_5.setText( str( d['role']['l'] ))
        self.stat_6.setText( str( d['role']['lk'] ))
        self.stat_7.setText( str( d['role']['prof'] ))
        self.stat_8.setText( str( d['gender']['m'] ))
        self.stat_9.setText( str( d['gender']['f'] ))
        
        # Prevent freezing
        QtCore.QCoreApplication.processEvents()
    
app = QtWidgets.QApplication(sys.argv)

window = WindowMain()
window.show()
app.exec()

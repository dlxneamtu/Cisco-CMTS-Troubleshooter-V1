__author__      = "Dan Neamtu"
__copyright__   = "Copyright 2014, Cisco Systems, Inc"
__credits__     = ["Dan Neamtu"]
__version__     = "1.0"
__status__      = "Development"

##########################################################################
## Class ConfigurationReader
## This is the Notebook tab that will be used for the Configuration Reader application function
###########################################################################
import wx
import wx.lib.scrolledpanel
import collections
import paramiko
import time
import threading
import ConfigTree
import sqlite3 as lite

class ConfigurationReader(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.get_dB_data()

        self.treePanel = wx.Panel(self) # this panel will have the configuration elements tree

############## Main Sizers and Displays ##############

        mainHSizer = wx.BoxSizer(wx.HORIZONTAL)
        loginTreeVSizer = wx.BoxSizer(wx.VERTICAL)
        configVSizer = wx.BoxSizer(wx.VERTICAL)
        outputVSizer = wx.BoxSizer(wx.VERTICAL)

        self.configDisplay = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.configDisplay.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))

        self.showOutputDisplay  = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.showOutputDisplay.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))

############## Mode of Operation ##############

        self.offlineRadio = wx.RadioButton(self, -1, 'Offline Mode   ')
        self.onlineRadio = wx.RadioButton(self, -1, 'Online Mode    ')
        self.offlineRadio.SetValue(True)
        self.okButton = wx.Button(self, -1, 'Load Configuration    ')

        operationModeBox = wx.StaticBox(self, label = "Operation Mode")
        operationModeBoxSizer = wx.StaticBoxSizer(operationModeBox, wx.HORIZONTAL)
        operationModeBoxSizer.Add(self.offlineRadio)
        operationModeBoxSizer.Add(self.onlineRadio)
        operationModeBoxSizer.Add(self.okButton)

        loginTreeVSizer.Add(operationModeBoxSizer)
        loginTreeVSizer.AddSpacer(2)

############## Login Credentials ##############

        self.deviceNameLabel = wx.StaticText(self, -1, 'Hostname:')
        self.deviceNameText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.usernameLabel = wx.StaticText(self, -1, 'Username:')
        self.usernameText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.passwordLabel = wx.StaticText(self, -1, 'Password:')
        self.passwordText = wx.TextCtrl(self, -1, size=(-1,-1), style = wx.TE_PASSWORD)
        self.enableLabel = wx.StaticText(self, -1, 'Enable:')
        self.enableText = wx.TextCtrl(self, -1, size=(-1,-1),style = wx.TE_PASSWORD)
        for item in [self.deviceNameText, self.usernameText, self.passwordText, self.enableText]:
            item.Enable(False)
            item.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))

        self.jumpServerCheckBox = wx.CheckBox(self, -1, 'Jumpserver')
        self.jumpServerLabel = wx.StaticText(self, -1, 'Hostname:')
        self.jumpServerNameText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.jumpUsernameLabel = wx.StaticText(self, -1, 'Username:')
        self.jumpUsernameText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.jumpPasswordLabel = wx.StaticText(self, -1, 'Password:')
        self.jumpPasswordText = wx.TextCtrl(self, -1, size=(-1,-1), style = wx.TE_PASSWORD)
        for item in [self.jumpServerNameText, self.jumpUsernameText, self.jumpPasswordText]:
            item.Enable(False)
            item.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))

        cmtsFlexGridSizer = wx.FlexGridSizer(cols=2, hgap=1)
        cmtsFlexGridSizer.Add(self.deviceNameLabel)
        cmtsFlexGridSizer.Add(self.deviceNameText)
        cmtsFlexGridSizer.Add(self.usernameLabel)
        cmtsFlexGridSizer.Add(self.usernameText)
        cmtsFlexGridSizer.Add(self.passwordLabel)
        cmtsFlexGridSizer.Add(self.passwordText)
        cmtsFlexGridSizer.Add(self.enableLabel)
        cmtsFlexGridSizer.Add(self.enableText)

        jumpserverFlexGridSizer = wx.FlexGridSizer(cols=2, vgap=1, hgap=1)
        jumpserverFlexGridSizer.Add(self.jumpServerCheckBox)
        jumpserverFlexGridSizer.Add(wx.StaticText(self, -1, ''))
        jumpserverFlexGridSizer.Add(self.jumpServerLabel)
        jumpserverFlexGridSizer.Add(self.jumpServerNameText)
        jumpserverFlexGridSizer.Add(self.jumpUsernameLabel)
        jumpserverFlexGridSizer.Add(self.jumpUsernameText)
        jumpserverFlexGridSizer.Add(self.jumpPasswordLabel)
        jumpserverFlexGridSizer.Add(self.jumpPasswordText)

        cmtsLoginBox = wx.StaticBox(self, label = "CMTS Login Details")
        cmtsLoginBoxSizer = wx.StaticBoxSizer(cmtsLoginBox, wx.VERTICAL)
        cmtsLoginBoxSizer.Add(cmtsFlexGridSizer)

        jumpserverLoginBox = wx.StaticBox(self, label = "Jumpserver Login Details")
        jumpserverLoginBoxSizer = wx.StaticBoxSizer(jumpserverLoginBox, wx.VERTICAL)
        jumpserverLoginBoxSizer.Add(jumpserverFlexGridSizer)

        loginHSizer = wx.BoxSizer(wx.HORIZONTAL)
        loginHSizer.Add(jumpserverLoginBoxSizer)
        loginHSizer.Add(cmtsLoginBoxSizer)

        loginTreeVSizer.Add(loginHSizer)

############## Tree Panel ##############

        self.tree = ConfigTree.ConfigTree(self.treePanel, id=-1, pos=wx.DefaultPosition, size=(400,-1),
                                                            style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT|wx.TR_DEFAULT_STYLE)

        self.tree.SetBackgroundColour((232, 232, 232, 255))
        treeBox = wx.StaticBox(self.treePanel, label = "Configuration Elements")
        treeBoxSizer = wx.StaticBoxSizer(treeBox, wx.VERTICAL)
        treeBoxSizer.Add(self.tree, proportion = 1)
        self.treePanel.SetSizer(treeBoxSizer)

        loginTreeVSizer.Add(self.treePanel, proportion=1)

############## Configuration Panel ##############

        self.deviceTitle = wx.StaticText(self, -1, '')
        self.emptyTitle = wx.StaticText(self, -1, '')
        configVSizer.Add(self.deviceTitle)
        configVSizer.Add(wx.StaticText(self, -1, '', size=(-1,25)))
        configVSizer.Add(self.configDisplay ,proportion=1, flag=wx.EXPAND)

############## Show Commands Panel ##############

        outputVSizer.Add(self.emptyTitle)
        outputVSizer.Add(wx.StaticText(self, -1, '', size=(-1,25)))
        outputVSizer.Add(self.showOutputDisplay ,proportion=1, flag=wx.EXPAND)

############## Main Sizer ##############

        mainHSizer.Add(loginTreeVSizer, flag=wx.EXPAND)
        mainHSizer.AddSpacer(4)
        mainHSizer.Add(configVSizer, proportion=3, flag=wx.EXPAND)
        mainHSizer.AddSpacer(2)
        mainHSizer.Add(outputVSizer, proportion=4, flag=wx.EXPAND)

        self.SetSizer(mainHSizer)

############## Events ##############

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.display_config_content)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.display_SSH_command_outputs)
        self.jumpServerCheckBox.Bind(wx.EVT_CHECKBOX, self.set_unset_jumpserver)
        self.okButton.Bind(wx.EVT_BUTTON, self.ok_button)
        for eachradio in [self.offlineRadio, self.onlineRadio]:
            self.Bind(wx.EVT_RADIOBUTTON, self.on_radio, eachradio)

############# Event actions #############

    def ok_button(self, e):
        if self.offlineRadio.GetValue() == True:
            self.load_config_file()
        elif self.onlineRadio.GetValue() == True:
            self.get_SSH_config_outputs()

    def set_unset_jumpserver(self, e):
        if self.jumpServerCheckBox.GetValue() == True:
            self.jumpServerNameText.Enable(True)
            self.jumpUsernameText.Enable(True)
            self.jumpPasswordText.Enable(True)
        else:
            self.jumpServerNameText.Enable(False)
            self.jumpUsernameText.Enable(False)
            self.jumpPasswordText.Enable(False)

    def on_radio(self, e):
        """
        The function is called when the radio box is checked. It enables the option while disabling the alternative
        """
        if e.GetEventObject().GetLabel() == self.offlineRadio.GetLabel():
            self.deviceNameText.Enable(False)
            self.usernameText.Enable(False)
            self.passwordText.Enable(False)
            self.enableText.Enable(False)

        elif e.GetEventObject().GetLabel() == self.onlineRadio.GetLabel():
            self.deviceNameText.Enable(True)
            self.usernameText.Enable(True)
            self.passwordText.Enable(True)
            self.enableText.Enable(True)

    def display_config_content(self,e):
        '''
        The function displays the configuration content relevant to the selected configuration element
        '''
        item =  self.tree.GetItemText(e.GetItem())
        if item != 'Remaining Config':
            self.configDisplay.SetValue(self.configElementsDict[item])
        else:
            self.configDisplay.SetValue(self.configElementsDict['Remaining Config'])
        e.Skip()

    def display_SSH_command_outputs(self,e):
        '''
        - displays the show command content relevant to the selected configuration element
        '''
        item =  self.tree.GetItemText(e.GetItem())

        if item != 'Remaining Config':
            self.showOutputDisplay.SetValue(self.showCommandOutputsDict[item])
        else:
            self.showOutputDisplay.SetValue('Not Applicable')
        e.Skip()

    def db_ID_to_Value(self, itemID, list):
        # This function looks into a list of 2d tuples obtained from a dB and returns the element associated to its ID
        for item in list:
            if item[0] == itemID:
                return item[1].encode('utf-8')

    def get_dB_data(self):
        # This function is used for setting up variables used throughout the program

        self.filename = ''
        self.configuration = ''
        self.output = ''
        self.start_substring = []
        self.end_substring = []
        self.include_substring = []

        #Database variables will be used to store tables with elements obtained from database
        self.dBCfgOutputTable = []
        self.dBShowOutputTable = []

        # Ordered dictionaries will be of type
        #   [configuration element:configuration content] and
        #   [configuration element:show command output content]
        self.configElementsDict = collections.OrderedDict()
        self.showCommandOutputsDict = collections.OrderedDict()

        #Gathering data from Database
        con = lite.connect('Cisco CMTS Troubleshooter Database.db')
        cur = con.cursor()

        with con:
            cur.execute("SELECT * FROM 'Configuration Item Table'")
            dBCfgItemTable = cur.fetchall()

        with con:
            cur.execute("SELECT * FROM 'Include String Table'")
            dBIncludeTable = cur.fetchall()

        #Building the list containing the elements necessary for displaying the configuration (item, start, end, include)
        with con:
            cur.execute("SELECT * FROM 'Configuration Output Table'")

            while True:
                includeTuple = ()
                row = cur.fetchone()
                if row == None:
                    break
                if type(row[3]) == int:
                    #Translating and adding to the list each element
                    self.dBCfgOutputTable.append([self.db_ID_to_Value(row[4],dBCfgItemTable),
                                                  row[1].encode('utf-8'), row[2].encode('utf-8'),
                                                  self.db_ID_to_Value(row[3],dBIncludeTable)])
                else:
                    if row[3].find(' , ') != -1:
                        tempInclude = row[3].split(' , ')
                    elif row[3].find(',') != -1:
                        tempInclude = row[3].split(',')
                    for item in tempInclude:
                        #Translating and adding to the list each element
                        includeTuple += (self.db_ID_to_Value(int(item),dBIncludeTable),)
                    self.dBCfgOutputTable.append([self.db_ID_to_Value(row[4],dBCfgItemTable),
                                                  row[1].encode('utf-8'), row[2].encode('utf-8'), includeTuple])

        with con:
            cur.execute("SELECT * FROM 'Show Command Table'")
            dBShowCommandTable = cur.fetchall()

        with con:
            cur.execute("SELECT * FROM 'Show Output Table'")

            while True:
                showTuple = ()
                row = cur.fetchone()

                if row == None:
                    break

                showTuple += (row[1].encode('utf-8'),) #Appends the helper (!Something) to the command list

                if type(row[2]) == unicode:
                    for item in row[2].encode('utf-8').split(','):
                        #print item,self.db_ID_to_Value(int(item), dBShowCommandTable)
                        showTuple += (self.db_ID_to_Value(int(item), dBShowCommandTable),)

                    self.dBShowOutputTable.append([self.db_ID_to_Value(row[3], dBCfgItemTable), showTuple])
                else:
                    showTuple += (self.db_ID_to_Value(row[2], dBShowCommandTable),)
                    self.dBShowOutputTable.append([self.db_ID_to_Value(row[3], dBCfgItemTable), showTuple])


        for item in self.dBCfgOutputTable:
            self.configElementsDict[item[0]] = '' # initialize the config file ordered dictionary
            self.start_substring.append(item[1]) # setup the start substring list used by copy_substring()
            self.end_substring.append(item[2]) # setup the end substring list used by copy_substring()
            self.include_substring.append(item[3]) # setup the include substring list used by copy_substring()

        for item  in self.dBShowOutputTable:
            self.showCommandOutputsDict[item[0]] = 'No information available yet' # initialize the show command ordered dictionary

    def populate_config_dict(self):
        for dict_item,start,end,include in zip(self.configElementsDict, self.start_substring, self.end_substring, self.include_substring):
        # Here I populate the dictionary with the config for each element
            if type(include) == tuple: # The case where include has multiple substrings to search for, I add them at the end
                self.configElementsDict[dict_item] = self.copy_substring(self.configuration, start, end, '')
                for include_string in include:
                    self.configElementsDict[dict_item] += self.copy_substring(self.configuration, 'No Display', '\n', include_string)
            else:
                self.configElementsDict[dict_item] = self.copy_substring(self.configuration,start,end,include)

    def populate_show_output_dict(self, startThreadIndex, endThreadIndex):
        '''
        - startThreadIndex = start position
        - endThreadIndex = end position
        - the above parameters are used to select a subset of commands to be executed per thread
        - the output from the show commands is gathered via SSH into a single file
        - populates the self.showCommandOutputsDict dictionary with the show output relevant to each
        configuration element
        - will be called by multiple separate threads that will start once the user introduces the device SSH
        details and presses OK.
        - threads will SSH to the device and execute subsets of all the show commands and store all output to a string
        - An identifier will be used to be able to pull the output content relevant to each configuration element
        '''
        commandSet = []
        for item  in self.dBShowOutputTable:
            self.showCommandOutputsDict[item[0]] = 'No information available yet' #Resetting the dictionary so that old
                        #information is not displayed until the new info is available (if user starts a new SSH session)

        for element in self.dBShowOutputTable[startThreadIndex:endThreadIndex]:   # for each element from the matrix
            commandSet.append(element[1])                                         # that contains the name & command
        completeOutputs = self.get_SSH_data(commandSet)

        for element in self.dBShowOutputTable[startThreadIndex:endThreadIndex]:
        # element is a tuple (output_element,(helper, command1,command2,..))
        # extracts the output between two helpers and appends it to the dictionary against the relevant output element
            if element != self.dBShowOutputTable[-1]:
                index = self.dBShowOutputTable.index(element)
                startPos = completeOutputs.find('!'+ element[0])
                end_pos = completeOutputs.find('!'+ self.dBShowOutputTable[index+1][0])
                self.showCommandOutputsDict[element[0]] = completeOutputs[startPos:end_pos]
            else:
                startPos = completeOutputs.find('!'+ element[0])
                self.showCommandOutputsDict[element[0]] = completeOutputs[startPos:]

    def load_config_file(self):
        """
        The function is called when the load button is pressed
        The function loads the configuration from the specified file, converts it into string and sets up the
        configuration content for each individual configuration element by calling the copy_substring() method
        """
        openFileDialog = wx.FileDialog(self, "Open File")
        openFileDialog.ShowModal()
        self.filename = openFileDialog.GetPath()
        deviceName = self.filename.split('/')
        deviceName = deviceName[len(deviceName)-1]

        with open(self.filename, 'r') as my_temp_file:
            self.configuration = str(my_temp_file.read()) #converting to string to find substrings easier
            my_temp_file.close()

        self.populate_config_dict() # populating the config content

        self.deviceTitle.SetLabel(deviceName)
        self.configDisplay.SetValue('Configuration loaded successfully!')

        # Here I manually populate the 'Remaining Config' item with configuration that was not allocated to other elements
        self.configElementsDict['Remaining Config'] = self.get_remaining_config()

        ConfigTree.ConfigTree.SetTreeElements(self.tree) # Setting the virtual tree
        self.delete_tree_item() # Deleting inactive tree items
        self.configDisplay.SetValue('Configuration loaded successfully!')

    def get_SSH_data(self, commandList):
        """
        Generic function to be used to extract data from the device via SSH. Returns the output
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        if self.jumpServerCheckBox.GetValue() == True:

            ssh.connect(hostname=self.jumpServerNameText.GetValue(),username=self.jumpUsernameText.GetValue(),
                        password=self.jumpPasswordText.GetValue(),allow_agent=False,look_for_keys=False)

            channel = ssh.invoke_shell()

            #Open SSH tunnel to the device from jumserver
            channel.send('ssh ' + self.usernameText.GetValue() + '@' + self.deviceNameText.GetValue() + '\n')
            time.sleep(1)
            channel.send(self.passwordText.GetValue() + '\n')
            time.sleep(1)
            channel.send('enable\n')
            time.sleep(1)
            channel.send(self.enableText.GetValue() + '\n')
            channel.send('ter len 0 \n')
            #Send commands and gather output
            for item in commandList:
                for subitem in item:
                    channel.send(subitem + "\n")
                    time.sleep(0.2)
            temp =''
            while channel.recv_ready():
                resp = channel.recv(200000)
                time.sleep(1)
                temp += resp
            return temp

        else:
            ssh.connect(hostname=self.deviceNameText.GetValue(),username=self.usernameText.GetValue(),
                        password=self.passwordText.GetValue(),allow_agent=False,look_for_keys=False)

            channel = ssh.invoke_shell()
            channel.send('enable\n')
            time.sleep(1)
            channel.send(self.enableText.GetValue() + '\n')
            channel.send('ter len 0 \n')
            for item in commandList:
                for subitem in item:
                    channel.send(subitem + "\n")
                    time.sleep(0.2)
            temp =''
            while channel.recv_ready(): #Populating the config
                resp = channel.recv(200000)
                time.sleep(1)
                #string = "".join(map(chr, resp)) # converting unicode to string
                temp += resp
            return temp

    def get_SSH_config_outputs(self):
        """
        The function is called when the device name is entered in the text box
        An ssh connection is opened to the device and its configuration is extracted
        The Configuration tree is updated and the configuration elements content prepared

        A separate thread starts in the background, meant to populate the show commands outputs in the second display
        """
        self.start_threads(12) # Starting threads
        self.configuration = self.get_SSH_data((('show run',),)) # The command send needs to be of type tuple
        self.populate_config_dict()  # populating the config contents
        self.deviceTitle.SetLabel(self.deviceNameText.GetValue())
        # Here I manually populate the 'Remaining Config' item with configuration that was not allocated to other elements
        self.configElementsDict['Remaining Config'] = self.get_remaining_config()
        ConfigTree.ConfigTree.SetTreeElements(self.tree) # Setting the virtual tree
        self.delete_tree_item() # Deleting inactive tree items
        self.configDisplay.SetValue('Configuration loaded successfully!')

    def start_threads(self,nrOfThreads):
        startIndex = 0
        endIndex = len(self.dBShowOutputTable)/nrOfThreads
        if nrOfThreads==1:
            thread = threading.Thread(target=self.populate_show_output_dict, args = (startIndex, endIndex))
                                                 # thread to run in the background for populating the show outputs
            thread.setDaemon(True)
            thread.start() # I start the thread that will call the self.populate_show_output_dict function
        else:
            for thread in range(0, nrOfThreads):
                #At each iteration I need to create a new list element to be able to store the command
                #subset to be executed as well as provide a new string to hold the outputs
                thread = threading.Thread(target=self.populate_show_output_dict, args = (startIndex,endIndex))
                                                 # thread to run in the background for populating the show outputs
                thread.setDaemon(True)
                thread.start() # I start the thread that will call the self.populate_show_output_dict function
                if nrOfThreads % 2 == 0:
                    startIndex = endIndex+1
                    endIndex = startIndex + len(self.dBShowOutputTable)/nrOfThreads
                else:
                    startIndex = endIndex+1
                    endIndex = startIndex + len(self.dBShowOutputTable)/nrOfThreads
                time.sleep(1)

    def get_remaining_config(self):
        # Returns all the configuration content that was not allocated to any other configuration item
        temp_config_list = self.configuration.splitlines()
        for key in self.configElementsDict.keys():
            temp_config_item_list = self.configElementsDict[key].splitlines()
            for item in temp_config_item_list:
                if item in temp_config_list:
                    temp_config_list.remove(item)
        return ','.join(temp_config_list).replace(',','\n!\n')

    def copy_substring(self, configuration, start, end, include):
        """
        The function takes as parameters:
            - configuration = the configuration file as string
            - start = the substring from which we need to start copying
            - end = the substring up to which we need to copy. This will typically be a '!'
        The function returns the configuration block found between and start and end sub-strings
        If the start substring repeats several times in the configuration (for example if we want to get all the fiber-nodes
        then we need to skip several end sub-strings until there is no longer a start sub-string to be found)
        """
        if include == '':  # The case where it is only provided start substring and end substring to search against
            result = ''
            startPosition = configuration.find(start)
            configuration = configuration[startPosition:]
            while startPosition != -1: #as long as the start sub-string exists in the config file we keep copying
                end_position = configuration.find(end) #search up to the first encounter of end
                result += configuration[:end_position+1] + "\n"
                configuration = configuration[end_position+1:]  #remove the previous chunk of config containing startPosition
                startPosition = configuration.find(start)
                configuration = configuration[startPosition:] #search from the first encounter of startPosition onwards
            if result == '':
                result = 'No Information'
            return result #return the substring found between startPosition and end_position

        else: # The case where it is also provided an include substring to search with
            result = ''
            startPosition = configuration.find(start)
            include_position = configuration.find(include)
            while startPosition != -1: #as long as the start sub-string exists in the config file we keep copying
                while include_position < startPosition:
                    configuration = configuration[include_position:]
                    end_position = configuration.find('\n')
                    result += configuration[:end_position] + "\n!\n"
                    configuration = configuration[end_position+1:]
                    startPosition = configuration.find(start)
                    include_position = configuration.find(include)

                configuration = configuration[startPosition:]
                end_position = configuration.find(end) #search up to the first encounter of end

                result += configuration[:end_position+1] + "\n!\n"
                configuration = configuration[end_position+1:]  #remove the previous chunk of config containing startPosition

                startPosition = configuration.find(start)
                include_position = configuration.find(include)

            while include_position != -1:
                # maybe I have include substring after the last start substring
                # I can also use this code to catch only include substrings, no start and end substrings
                configuration = configuration[include_position:]
                end_position = configuration.find('\n')
                result += configuration[:end_position] + "\n!\n"
                configuration = configuration[end_position+1:]
                include_position = configuration.find(include)
            if result == '':
                result = 'No Information'
            return result #return the substring found between startPosition and end_position

    def delete_tree_item(self):
        # The function goes through each three item and if its associated configuration is blank, the item is removed from
        # the tree
        for item in ConfigTree.ConfigTree.GetTreeElements(self.tree):
            if self.configElementsDict[item] == 'No Information':
                ConfigTree.ConfigTree.UpdateTreeElements(self.tree, item)
        ConfigTree.ConfigTree.RefreshItems(self.tree)

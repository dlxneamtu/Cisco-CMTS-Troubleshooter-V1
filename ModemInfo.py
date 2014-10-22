__author__      = "Dan Neamtu"
__copyright__   = "Copyright 2014, Cisco Systems, Inc"
__credits__     = ["Dan Neamtu"]
__version__     = "1.0"
__status__      = "Development"

import wx
import sqlite3 as lite
import threading
import time
import paramiko
from pyparsing import Word,Literal,alphas,alphanums,Group,nums

##########################################################################
## Class Modem Info
## This is the Notebook tab that will be used for the modem info application function
###########################################################################

class ModemInfo(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        self.macIPAddress = ''
    # Login Information
        loginStaticBox = wx.StaticBox(self, label = "Login details")
        loginStaticBoxSizer = wx.StaticBoxSizer(loginStaticBox, wx.HORIZONTAL)

        loginFlexGridSizerSizer = wx.FlexGridSizer(cols=2, hgap=1, vgap=2)
        deviceLabel = wx.StaticText(self, -1, 'Hostname:')
        self.deviceNameText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.deviceNameText.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        usernameLabel = wx.StaticText(self, -1, 'Username:')
        self.usernameText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.usernameText.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        passwordLabel = wx.StaticText(self, -1, 'Password:')
        self.passwordText = wx.TextCtrl(self, -1, size=(-1,-1), style = wx.TE_PASSWORD)
        self.passwordText.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        enableLabel = wx.StaticText(self, -1, 'Enable:')
        self.enableText = wx.TextCtrl(self, -1, size=(-1,-1),style = wx.TE_PASSWORD)
        self.enableText.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))

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

        loginButton = wx.Button(self, -1, 'OK')
        loginFlexGridSizerSizer.Add(deviceLabel)
        loginFlexGridSizerSizer.Add(self.deviceNameText)
        loginFlexGridSizerSizer.Add(usernameLabel)
        loginFlexGridSizerSizer.Add(self.usernameText)
        loginFlexGridSizerSizer.Add(passwordLabel)
        loginFlexGridSizerSizer.Add(self.passwordText)
        loginFlexGridSizerSizer.Add(enableLabel)
        loginFlexGridSizerSizer.Add(self.enableText)

        loginFlexGridSizerSizer.Add(self.jumpServerCheckBox)
        loginFlexGridSizerSizer.Add(wx.StaticText(self, -1, ''))
        loginFlexGridSizerSizer.Add(self.jumpServerLabel)
        loginFlexGridSizerSizer.Add(self.jumpServerNameText)
        loginFlexGridSizerSizer.Add(self.jumpUsernameLabel)
        loginFlexGridSizerSizer.Add(self.jumpUsernameText)
        loginFlexGridSizerSizer.Add(self.jumpPasswordLabel)
        loginFlexGridSizerSizer.Add(self.jumpPasswordText)


        loginFlexGridSizerSizer.Add(loginButton)
        loginStaticBoxSizer.Add(loginFlexGridSizerSizer)
        loginStaticBoxSizer.AddSpacer(3)


    # Modem MAC/IP details
        macIPStaticBox = wx.StaticBox(self, label = "MAC/IP Address")
        macIPStaticBoxSizer = wx.StaticBoxSizer(macIPStaticBox, wx.HORIZONTAL)
        self.macIPOKButton = wx.Button(self, -1, 'OK')
        self.macIPOKButton.Enable(False)
        self.macIPText = wx.TextCtrl(self, -1, size=(-1,-1))
        self.macIPText.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.macIPText.Enable(False)
        macIPStaticBoxSizer.Add(self.macIPOKButton, proportion=0, flag=wx.ALL)
        macIPStaticBoxSizer.AddSpacer(2)
        macIPStaticBoxSizer.Add(self.macIPText, proportion=0, flag=wx.ALL)
        macIPStaticBoxSizer.AddSpacer(2)
    # Options details
        optionsStaticBox = wx.StaticBox(self, label = "Options")
        optionsStaticBoxSizer = wx.StaticBoxSizer(optionsStaticBox, wx.HORIZONTAL)
        self.phyRadio = wx.RadioButton(self, -1, 'Phy')
        self.sfRadio = wx.RadioButton(self, -1, 'Service Flow')
        self.classifierRadio = wx.RadioButton(self, -1, 'Classifier')
        self.usdsStatusRadio = wx.RadioButton(self, -1, 'US/DS status')
        self.qosRadio = wx.RadioButton(self, -1, 'QoS')
        self.flapRadio = wx.RadioButton(self, -1, 'Flap')
        self.bpiRadio = wx.RadioButton(self, -1, 'BPI')
        self.resiliencyRadio = wx.RadioButton(self, -1, 'Resiliency')
        self.ipv6Radio = wx.RadioButton(self, -1, 'IPv6')
        self.connectivityRadio = wx.RadioButton(self, -1, 'Connectivity')
        self.Radio11 = wx.RadioButton(self, -1, 'Radio11(tbd)')
        self.Radio12 = wx.RadioButton(self, -1, 'Radio12(tbd)')
        self.Radio13 = wx.RadioButton(self, -1, 'Radio13(tbd)')
        self.Radio14 = wx.RadioButton(self, -1, 'Radio14(tbd)')
        self.Radio15 = wx.RadioButton(self, -1, 'Radio15(tbd)')
        for radio in [self.phyRadio,self.sfRadio,self.classifierRadio,self.usdsStatusRadio,self.qosRadio,self.flapRadio,
                      self.bpiRadio,self.resiliencyRadio,self.ipv6Radio,self.connectivityRadio,self.Radio11,self.Radio12,
                      self.Radio13,self.Radio14,self.Radio15]:
            radio.Enable(False)
        
        optionsBoxSizer1 = wx.BoxSizer(wx.VERTICAL)
        optionsBoxSizer2 = wx.BoxSizer(wx.VERTICAL)
        optionsBoxSizer3 = wx.BoxSizer(wx.VERTICAL)

        optionsBoxSizer1.Add(self.sfRadio)
        optionsBoxSizer1.Add(self.classifierRadio)
        optionsBoxSizer1.Add(self.usdsStatusRadio)
        optionsBoxSizer1.Add(self.connectivityRadio)
        optionsBoxSizer1.Add(self.resiliencyRadio)
        optionsBoxSizer2.Add(self.qosRadio)
        optionsBoxSizer2.Add(self.phyRadio)
        optionsBoxSizer2.Add(self.flapRadio)
        optionsBoxSizer2.Add(self.bpiRadio)
        optionsBoxSizer2.Add(self.ipv6Radio)
        optionsBoxSizer3.Add(self.Radio11)
        optionsBoxSizer3.Add(self.Radio12)
        optionsBoxSizer3.Add(self.Radio13)
        optionsBoxSizer3.Add(self.Radio14)
        optionsBoxSizer3.Add(self.Radio15)
        
        optionsStaticBoxSizer.Add(optionsBoxSizer1)
        optionsStaticBoxSizer.AddSpacer(5)
        optionsStaticBoxSizer.Add(optionsBoxSizer2)
        optionsStaticBoxSizer.AddSpacer(5)
        optionsStaticBoxSizer.Add(optionsBoxSizer3)

    # General information details
        macLabel = wx.StaticText(self, label = 'MAC Address')
        self.macLabelValue = wx.StaticText(self, label = 'Test Information String')
        IPLabel = wx.StaticText(self, label = 'IP Address')
        self.IPLabelValue = wx.StaticText(self, label = 'Test Information String')
        primaryChLabel = wx.StaticText(self, label = 'Primary Channel')
        self.primaryChLabelValue = wx.StaticText(self, label = 'Test Information String')
        mdLabel = wx.StaticText(self, label = 'MAC Domain')
        self.mdLabelValue = wx.StaticText(self, label = 'Test Information String')
        sidLabel = wx.StaticText(self, label = 'SID')
        self.sidLabelValue = wx.StaticText(self, label = 'Test Information String')
        modelLabel = wx.StaticText(self, label = 'Model')
        self.modelLabelValue = wx.StaticText(self, label = 'Test Information String')
        vendorLabel = wx.StaticText(self, label = 'Vendor')
        self.vendorLabelValue = wx.StaticText(self, label = 'Test Information String')
        USSFIDLabel = wx.StaticText(self, label = 'US SFID')
        self.USSFIDLabelValue = wx.StaticText(self, label = 'Test Information String')
        DSSFIDLabel = wx.StaticText(self, label = 'DS SFID')
        self.DSSFIDLabelValue = wx.StaticText(self, label = 'Test Information String')
        hostLabel = wx.StaticText(self, label = 'Hosts')
        self.hostLabelValue = wx.StaticText(self, label = 'Test Information String')
        classifiersLabel = wx.StaticText(self, label = 'SFs w\ Classifiers')
        self.classifiersLabelValue = wx.StaticText(self, label = 'Test Information String')
        usXdsLabel = wx.StaticText(self, label = 'DS x US')
        self.usXdsLabelValue = wx.StaticText(self, label = 'Test Information String')
        mtcLabel = wx.StaticText(self, label = 'MTC Mode')
        self.mtcLabelValue = wx.StaticText(self, label = 'Test Information String')
        generalInfoFlexGridSizer = wx.FlexGridSizer(cols=2, hgap=1, vgap=3)
        generalInfoFlexGridSizer.Add(macLabel)
        generalInfoFlexGridSizer.Add(self.macLabelValue)
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(IPLabel)
        generalInfoFlexGridSizer.Add(self.IPLabelValue)
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(primaryChLabel)
        generalInfoFlexGridSizer.Add(self.primaryChLabelValue)
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(mdLabel)
        generalInfoFlexGridSizer.Add(self.mdLabelValue)
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(sidLabel)
        generalInfoFlexGridSizer.Add(self.sidLabelValue)
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(usXdsLabel)
        generalInfoFlexGridSizer.Add(self.usXdsLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(mtcLabel)
        generalInfoFlexGridSizer.Add(self.mtcLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(USSFIDLabel)
        generalInfoFlexGridSizer.Add(self.USSFIDLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(DSSFIDLabel)
        generalInfoFlexGridSizer.Add(self.DSSFIDLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(hostLabel)
        generalInfoFlexGridSizer.Add(self.hostLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(classifiersLabel)
        generalInfoFlexGridSizer.Add(self.classifiersLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(modelLabel)
        generalInfoFlexGridSizer.Add(self.modelLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoFlexGridSizer.Add(vendorLabel)
        generalInfoFlexGridSizer.Add(self.vendorLabelValue )
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (110,2)))
        generalInfoFlexGridSizer.Add(wx.StaticLine(self,-1,(-1,-1), (150,2)))
        generalInfoStaticBox = wx.StaticBox(self, label = "General Information")
        generalInfoStaticBoxSizer = wx.StaticBoxSizer(generalInfoStaticBox, wx.HORIZONTAL)
        generalInfoStaticBoxSizer.Add(generalInfoFlexGridSizer)

# US/DS channel details
        usChannelStaticBox = wx.StaticBox(self, label = "US Channels")
        usChannelStaticBoxSizer = wx.StaticBoxSizer(usChannelStaticBox, wx.HORIZONTAL)
        self.usChannelValue = wx.TextCtrl(self, -1,'US Channels',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.usChannelValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        usChannelStaticBoxSizer.Add(self.usChannelValue, proportion=1, flag=wx.EXPAND)

        dsChannelStaticBox = wx.StaticBox(self, label = "DS Channels")
        dsChannelStaticBoxSizer = wx.StaticBoxSizer(dsChannelStaticBox, wx.HORIZONTAL)
        self.dsChannelValue = wx.TextCtrl(self, -1,'DS Channels',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.dsChannelValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        dsChannelStaticBoxSizer.Add(self.dsChannelValue, proportion=1, flag=wx.EXPAND)

# SCM Summary total
        summaryStaticBox = wx.StaticBox(self, label = "Modem Count Summary")
        self.summaryStaticBoxSizer = wx.StaticBoxSizer(summaryStaticBox, wx.HORIZONTAL)
        self.summaryValue = wx.TextCtrl(self, -1,'Modem Count Summary Details',size=(-1,-1), style = wx.TE_READONLY|
                                                                                                     wx.TE_MULTILINE)
        self.summaryValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.summaryStaticBoxSizer.Add(self.summaryValue, proportion=1, flag=wx.EXPAND)

# Phy channel details
        phyStaticBox = wx.StaticBox(self, label = "Phy Details")
        phyStaticBoxSizer = wx.StaticBoxSizer(phyStaticBox, wx.HORIZONTAL)
        self.phyValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.phyValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        phyStaticBoxSizer.Add(self.phyValue, proportion=1, flag=wx.EXPAND)

# Service Flow
        usServiceFlowStaticBox = wx.StaticBox(self, label = "US Service Flows")
        self.usServiceFlowStaticBoxSizer = wx.StaticBoxSizer(usServiceFlowStaticBox, wx.HORIZONTAL)
        self.usServiceFlowValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.usServiceFlowValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.usServiceFlowStaticBoxSizer.Add(self.usServiceFlowValue, proportion=1, flag=wx.EXPAND)

        dsServiceFlowStaticBox = wx.StaticBox(self, label = "DS Service Flows")
        self.dsServiceFlowStaticBoxSizer = wx.StaticBoxSizer(dsServiceFlowStaticBox, wx.HORIZONTAL)
        self.dsServiceFlowValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.dsServiceFlowValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.dsServiceFlowStaticBoxSizer.Add(self.dsServiceFlowValue, proportion=1, flag=wx.EXPAND)

# Classifiers
        classifiersStaticBox = wx.StaticBox(self, label = "Classifiers")
        self.classifiersStaticBoxSizer = wx.StaticBoxSizer(classifiersStaticBox, wx.HORIZONTAL)
        self.detailedClassifiersValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.detailedClassifiersValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.classifiersStaticBoxSizer.Add(self.detailedClassifiersValue, proportion=1, flag=wx.EXPAND)

# QoS channel details
        qosStaticBox = wx.StaticBox(self, label = "QOS Details")
        qosStaticBoxSizer = wx.StaticBoxSizer(qosStaticBox, wx.HORIZONTAL)
        self.qosValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.qosValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        qosStaticBoxSizer.Add(self.qosValue, proportion=1, flag=wx.EXPAND)

# Flap
        flapStaticBox = wx.StaticBox(self, label = "Flap")
        self.flapStaticBoxSizer = wx.StaticBoxSizer(flapStaticBox, wx.HORIZONTAL)
        self.flapValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.flapValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.flapStaticBoxSizer.Add(self.flapValue, proportion=1, flag=wx.EXPAND)

# BPI
        bpiStaticBox = wx.StaticBox(self, label = "BPI")
        self.bpiStaticBoxSizer = wx.StaticBoxSizer(bpiStaticBox, wx.HORIZONTAL)
        self.bpiValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.bpiValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.bpiStaticBoxSizer.Add(self.bpiValue, proportion=1, flag=wx.EXPAND)

# Resiliency
        resiliencyStaticBox = wx.StaticBox(self, label = "Resiliency")
        self.resiliencyStaticBoxSizer = wx.StaticBoxSizer(resiliencyStaticBox, wx.HORIZONTAL)
        self.resiliencyValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.resiliencyValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.resiliencyStaticBoxSizer.Add(self.resiliencyValue, proportion=1, flag=wx.EXPAND)

# IPv6
        ipv6StaticBox = wx.StaticBox(self, label = "IPv6")
        self.ipv6StaticBoxSizer = wx.StaticBoxSizer(ipv6StaticBox, wx.HORIZONTAL)
        self.ipv6Value = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.ipv6Value.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.ipv6StaticBoxSizer.Add(self.ipv6Value, proportion=1, flag=wx.EXPAND)

# Connectivity
        connectivityStaticBox = wx.StaticBox(self, label = "Connectivity")
        self.connectivityStaticBoxSizer = wx.StaticBoxSizer(connectivityStaticBox, wx.HORIZONTAL)
        self.connectivityValue = wx.TextCtrl(self, -1,'',size=(-1,-1), style = wx.TE_READONLY|wx.TE_MULTILINE)
        self.connectivityValue.SetFont(wx.Font(12,wx.MODERN,wx.NORMAL,wx.NORMAL))
        self.connectivityStaticBoxSizer.Add(self.connectivityValue, proportion=1, flag=wx.EXPAND)

# Main frame layout
        secVSizerLeft = wx.BoxSizer(wx.VERTICAL)
        secVSizerLeft.Add(loginStaticBoxSizer)
        secVSizerLeft.Add(macIPStaticBoxSizer)
        secVSizerLeft.Add(optionsStaticBoxSizer)
        secVSizerLeft.Add(generalInfoStaticBoxSizer)

        self.secVSizerSummary = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerSummary.Add(self.summaryStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerSummary = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerSummary.Add(self.summaryStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerPhy = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerPhy.Add(phyStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerServiceFlow = wx.BoxSizer(wx.HORIZONTAL)
        self.secVSizerServiceFlow.Add(self.usServiceFlowStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerServiceFlow.Add(self.dsServiceFlowStaticBoxSizer, proportion=1, flag=wx.EXPAND)

        self.secVSizerClassifier = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerClassifier.Add(self.classifiersStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        #self.secVSizerUsDsStatus = wx.BoxSizer(wx.VERTICAL)
        #self.secVSizerUsDsStatus.Add(self.usDsStatusStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerFlap = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerFlap.Add(self.flapStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerBpi = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerBpi.Add(self.bpiStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerResiliency = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerResiliency.Add(self.resiliencyStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerIPv6 = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerIPv6.Add(self.ipv6StaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerConnectivity = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerConnectivity.Add(self.connectivityStaticBoxSizer, proportion=1, flag=wx.EXPAND)

        self.secVSizerUsDs = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerUsDs.Add(usChannelStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerUsDs.Add(dsChannelStaticBoxSizer, proportion=1, flag=wx.EXPAND)
        self.secVSizerQos = wx.BoxSizer(wx.VERTICAL)
        self.secVSizerQos.Add(qosStaticBoxSizer, proportion=1, flag=wx.EXPAND)

        self.sizersList = [self.secVSizerPhy,self.secVSizerBpi, self.secVSizerClassifier, self.secVSizerFlap, self.secVSizerQos,
                           self.secVSizerResiliency, self.secVSizerServiceFlow, self.secVSizerUsDs,self.secVSizerSummary,
                           self.secVSizerIPv6, self.secVSizerConnectivity]

        self.mainHSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainHSizer.Add(secVSizerLeft, flag=wx.EXPAND)
        self.mainHSizer.AddSpacer(10)
        self.mainHSizer.Add(self.secVSizerSummary, proportion=1, flag=wx.EXPAND)

        for sizer in self.sizersList:
            if sizer == self.secVSizerSummary:
                pass
            else:
                self.mainHSizer.Add(sizer, proportion=1, flag=wx.EXPAND)
                self.mainHSizer.Hide(sizer)

        self.SetSizer(self.mainHSizer) #Sizer is set on the panel

        #Events
        loginButton.Bind(wx.EVT_BUTTON, self.device_login)
        self.macIPOKButton.Bind(wx.EVT_BUTTON, self.setup_data)
        self.phyRadio.Bind(wx.EVT_RADIOBUTTON, self.on_phy)
        self.sfRadio.Bind(wx.EVT_RADIOBUTTON, self.on_service_flow)
        self.classifierRadio.Bind(wx.EVT_RADIOBUTTON, self.on_classifier)
        self.usdsStatusRadio.Bind(wx.EVT_RADIOBUTTON, self.on_us_ds_status)
        self.qosRadio.Bind(wx.EVT_RADIOBUTTON, self.on_qos)
        self.flapRadio.Bind(wx.EVT_RADIOBUTTON, self.on_flap)
        self.bpiRadio.Bind(wx.EVT_RADIOBUTTON, self.on_bpi)
        self.resiliencyRadio.Bind(wx.EVT_RADIOBUTTON, self.on_resiliency)
        self.ipv6Radio.Bind(wx.EVT_RADIOBUTTON, self.on_ipv6)
        self.connectivityRadio.Bind(wx.EVT_RADIOBUTTON, self.on_connectivity)
        self.jumpServerCheckBox.Bind(wx.EVT_CHECKBOX, self.set_unset_jumpserver)

    def set_unset_jumpserver(self, e):
        if self.jumpServerCheckBox.GetValue() == True:
            self.jumpServerNameText.Enable(True)
            self.jumpUsernameText.Enable(True)
            self.jumpPasswordText.Enable(True)
        else:
            self.jumpServerNameText.Enable(False)
            self.jumpUsernameText.Enable(False)
            self.jumpPasswordText.Enable(False)

    def on_phy(self, e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerPhy)
        self.mainHSizer.Layout()
        self.phyValue.SetValue(self.modemCommandOutputsDict['phy'])

    def on_service_flow(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerServiceFlow)
        self.mainHSizer.Layout()
        self.usServiceFlowValue.SetValue(self.modemCommandOutputsDict['usServiceFlow'])
        self.dsServiceFlowValue.SetValue(self.modemCommandOutputsDict['dsServiceFlow'])

    def on_classifier(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerClassifier)
        self.mainHSizer.Layout()
        self.detailedClassifiersValue.SetValue(self.modemCommandOutputsDict['detailedClassifiers'])

    def on_us_ds_status(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerUsDs)
        self.mainHSizer.Layout()
        self.usChannelValue.SetValue(self.modemCommandOutputsDict['usChannels'])
        self.dsChannelValue.SetValue(self.modemCommandOutputsDict['dsChannels'])

    def on_qos(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerQos)
        self.mainHSizer.Layout()
        self.qosValue.SetValue(self.modemCommandOutputsDict['qos'])

    def on_flap(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerFlap)
        self.mainHSizer.Layout()
        self.flapValue.SetValue(self.modemCommandOutputsDict['flap'])

    def on_bpi(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerBpi)
        self.mainHSizer.Layout()
        self.bpiValue.SetValue(self.modemCommandOutputsDict['bpi'])

    def on_resiliency(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerResiliency)
        self.mainHSizer.Layout()
        self.resiliencyValue.SetValue(self.modemCommandOutputsDict['resiliency'])

    def on_ipv6(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerIPv6)
        self.mainHSizer.Layout()
        self.ipv6Value.SetValue(self.modemCommandOutputsDict['ipv6'])

    def on_connectivity(self,e):
        for sizer in self.sizersList:
            if self.mainHSizer.IsShown(sizer) == True:
                self.mainHSizer.Hide(sizer)
        self.mainHSizer.Show(self.secVSizerConnectivity)
        self.mainHSizer.Layout()
        self.connectivityValue.SetValue(self.modemCommandOutputsDict['connectivity'])

    def device_login(self,e):
        self.macIPOKButton.Enable(True)
        self.macIPText.Enable(True)
        self.summaryValue.SetValue(self.get_SSH_data((('scm summary total',),)))

    def setup_data(self,e):
    # List of format [modem output element, helper, (command1, command2,...)]
        self.dBModemCommandTable = []
    # Dictionary will be of type [modem output element:show command output content] and will be used to populate the GUI
        self.modemCommandOutputsDict = {}
        #Gathering commands data from Database
        con = lite.connect('Cisco CMTS Troubleshooter Database.db')
        cur = con.cursor()

        with con:
            cur.execute("SELECT * FROM 'Show Command Table'")
            self.dBShowCommandTable = cur.fetchall()
        with con:
            cur.execute("SELECT * FROM 'Modem Show Command Table'")
            while True:
                row = cur.fetchone()
                command = [] # [!helper, command1, command2,...]
                if row == None:
                    break
                command.append(row[2].encode('utf-8')) #Appends the helper (!Something) to the command list. This will
                # be used to extract certain outputs from the output file
                if type(row[1]) == unicode: # There is more than one command for an output element needed
                    for item in row[1].encode('utf-8').split(','): #split the unicode list of command IDs
                        command.append(self.db_ID_to_Value(int(item), self.dBShowCommandTable)) # convert command ID to
                        # command value and append each to a temporary list
                        if '&mac' in command[-1]: # I need to convert the key word to the mac value introduced in GUI
                            command[-1] = command[-1].replace('&mac', self.macIPText.GetValue()) #insert the mac address
                    self.dBModemCommandTable.append([row[0].encode('utf-8'),command]) # append the element and the
                        # corresponding command and set of commands to the dictionary

                else: #Only one command for an output element hence do the same stuff as above, but simpler
                    command.append(self.db_ID_to_Value(int(row[1]), self.dBShowCommandTable))
                    if '&mac' in command[-1]:
                        command[-1] = command[-1].replace('&mac', self.macIPText.GetValue())
                    self.dBModemCommandTable.append([row[0].encode('utf-8'),command])

        for item in self.dBModemCommandTable:
            self.modemCommandOutputsDict[item[0]] = 'Not available' # initialize the output dictionary
        self.populate_show_output_dict()
        self.display_general_info()
        for radio in [self.phyRadio,self.sfRadio,self.classifierRadio,self.usdsStatusRadio,self.qosRadio,self.flapRadio,
                      self.bpiRadio,self.resiliencyRadio,self.ipv6Radio,self.connectivityRadio,self.Radio11,self.Radio12,
                      self.Radio13,self.Radio14,self.Radio15]:
            radio.Enable(True)

    def populate_show_output_dict(self):
        '''
        - walk the command list and
        '''
        commandSet = []
        for element in self.dBModemCommandTable:
            if element[1] in commandSet:
                pass
            else:
                commandSet.append(element[1])
        completeOutputs = self.get_SSH_data(commandSet)

        mac = Group(Literal('MAC Address') + ':') + Group(Word(alphanums, exact=4) + '.' + Word(alphanums, exact=4) +
                                                          '.' + Word(alphanums, exact=4)) + Literal('IP')
        IP = Group(Literal('IP Address') + ':') + Group(Word(nums, max=3) + '.' + Word(nums, max=3) + '.' +
                                                                Word(nums, max=3) + '.' + Word(nums, max=3))
        primary = Group(Literal('Primary Downstream') + ':') + Group(Word(alphanums) + '/' + Word(alphanums) +
                                                            '/' + Word(alphanums) + ':' + Word(alphanums))
        sid = Group(Literal('Prim Sid') + ':') + Word(nums, max=4)
        mtc = Group(Literal('Multi-Transmit Channel Mode') + ':') + Word(alphas, exact=1)
        md = Group(Literal('Host Interface') + ':') + Group(Word(alphanums) + '/' + Word(alphanums) +
                                                                    '/' + Word(alphanums))
        host = Literal('Access-group') + Group(Word(nums, max=4) + '.' + Word(alphanums, exact=4) + '.' + Word(alphanums, exact=4))
        ussfid = Word(nums, max=4) + Literal('US') + Word(alphas) + Word(alphanums+'/') + Word(alphanums+'/') + \
                 Word(nums) + Word(nums) + Word(nums) + Word(nums) + Word(nums)
        dssfid = Word(nums, max=4) + Literal('DS') + Word(alphas) + Word(alphanums+'/') + Word(alphanums+'/') + \
                 Word(nums) + Word(nums) + Word(nums) + Word(nums) + Word(nums)
        classifiers = Word(nums) + Word(nums) + Group(Word(alphanums, exact=4) + '.' + Word(alphanums, exact=4) + '.' +
                                                     Word(alphanums, exact=4))
        dsXus = Word('w-online(pkt)') + Group(Word(nums,max=2) + 'x' + Word(nums,max=2))
        vendor = Literal('VENDOR:') + Word(alphanums+'-')
        model = Literal('MODEL:') + Word(alphanums+'-')


    # Extract specific information from the output file
        for element,key in zip([mac,IP,primary,sid,mtc,md,host,ussfid,dssfid,classifiers,dsXus,vendor,model],
                               ['mac','IP','primary','sid','mtc','md','host','ussfid','dssfid','classifiers',
                                'dsXus','vendor','model']):
            temp = []
            if element==classifiers:
                try:
                    temp.append(' '.join((''.join(element.searchString(completeOutputs)[0][0]),
                                          ''.join(element.searchString(completeOutputs)[0][1]))))
                except IndexError:
                    pass
            elif element==ussfid or element==dssfid:
                try:
                    temp.append(''.join(element.searchString(completeOutputs)[0][0]))
                except IndexError:
                    pass
            else:
                try:
                    temp.append(''.join(element.searchString(completeOutputs)[0][1]))
                except IndexError:
                    pass
            self.modemCommandOutputsDict[key] = ' '.join(temp)
        self.start_threads()

    # Extract a block of output from the output file
        for key in ['usChannels','dsChannels','qos','flap','bpi','ipv6','phy','resiliency',
                    'connectivity','detailedClassifiers']:
            startIndex = completeOutputs.index('!none'+key)
            temp = completeOutputs[startIndex+5:]
            try:
                endIndex = temp.index('!none')
                #Manually fixing the display for these two command outputs
                if key == 'usChannels':
                    self.modemCommandOutputsDict[key] = self.deviceNameText.GetValue() + '#show cable modem '+ \
                                                        self.modemCommandOutputsDict['mac'] + \
                                   ' ver | in Upstream Channel|Ranging Status|Upstream SNR|Received Power|Reported ' \
                                                        'Transmit Power|Timing Offset\n' + \
                                                        '\n'.join(temp[:endIndex].splitlines()[2:])
                elif key == 'dsChannels':
                    self.modemCommandOutputsDict[key] = self.deviceNameText.GetValue() + '#show cable modem '+ \
                                                        self.modemCommandOutputsDict['mac'] + \
                                                        ' wideband rcs-status | in RF  :|Status\n' + \
                                                        '\n'.join(temp[:endIndex].splitlines()[2:])

                else:
                    self.modemCommandOutputsDict[key] = '\n'.join(temp[:endIndex].splitlines()[1:])

            #Handling the case where this is the last command output in the file
            except ValueError:
                #Manually fixing the display for these two command outputs
                if key == 'usChannels':
                    self.modemCommandOutputsDict[key] = self.deviceNameText.GetValue() + '#show cable modem '+ \
                                                        self.modemCommandOutputsDict['mac'] + \
                                   ' ver | in Upstream Channel|Ranging Status|Upstream SNR|Received Power|Reported ' \
                                                        'Transmit Power|Timing Offset\n' + \
                                                        '\n'.join(temp.splitlines()[2:])
                elif key == 'dsChannels':
                    self.modemCommandOutputsDict[key] = self.deviceNameText.GetValue() + '#show cable modem '+ \
                                                        self.modemCommandOutputsDict['mac'] + \
                                                        ' wideband rcs-status | in RF  :|Status\n' + \
                                                        '\n'.join(temp.splitlines()[2:])
                else:
                    self.modemCommandOutputsDict[key] = '\n'.join(temp.splitlines()[1:])

    def start_threads(self):
        thread = threading.Thread(target=self.get_SF_output) # thread to run in the background for getting SF info
        thread.setDaemon(True)
        thread.start() # I start the thread that will call the self.populate_show_output_dict function

    def get_SF_output(self):

        sfCommandSet = []
        con = lite.connect('Cisco CMTS Troubleshooter Database.db')
        cur = con.cursor()

        with con:
            cur.execute('SELECT * FROM "Modem Show Command Table" WHERE "Output Element" = "usServiceFlow"')
            row = cur.fetchone()
            command = []
            command.append(row[2].encode('utf-8'))

            for id in self.modemCommandOutputsDict['ussfid'].split():
                for item in row[1].encode('utf-8').split(','):
                    command.append(self.db_ID_to_Value(int(item), self.dBShowCommandTable))
                    if '&md' in command[-1]:
                        command[-1] = command[-1].replace('&md', self.modemCommandOutputsDict['md'])
                    if '&sf' in command[-1]:
                        command[-1] = command[-1].replace('&sf', id)

            sfCommandSet.append(command)

        with con:
            cur.execute('SELECT * FROM "Modem Show Command Table" WHERE "Output Element" = "dsServiceFlow"')
            row = cur.fetchone()
            command = []
            command.append(row[2].encode('utf-8'))

            for id in self.modemCommandOutputsDict['dssfid'].split():
                for item in row[1].encode('utf-8').split(','):
                    command.append(self.db_ID_to_Value(int(item), self.dBShowCommandTable))
                    if '&md' in command[-1]:
                        command[-1] = command[-1].replace('&md', self.modemCommandOutputsDict['md'])
                    if '&sf' in command[-1]:
                        command[-1] = command[-1].replace('&sf', id)

            sfCommandSet.append(command)

        sfOutput = self.get_SSH_data(sfCommandSet)

        for key in ['usServiceFlow','dsServiceFlow']:
            startIndex = sfOutput.index('!none'+key)
            temp = sfOutput[startIndex+5:]
            try:
                endIndex = temp.index('!none')
                self.modemCommandOutputsDict[key] = '\n'.join(temp[:endIndex].splitlines()[1:])
            except ValueError:
                self.modemCommandOutputsDict[key] = '\n'.join(temp.splitlines()[1:])

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
            channel.send('enable\n')
            time.sleep(1)
            channel.send(self.enableText.GetValue() + '\n')
            channel.send('ter len 0 \n')
            for item in commandList:
                for subitem in item:
                    channel.send(subitem + "\n")
                    time.sleep(0.2)
            temp =''
            while channel.recv_ready():
                resp = channel.recv(200000)
                time.sleep(1)
                #string = "".join(map(chr, resp)) # converting unicode to string
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
            while channel.recv_ready():
                resp = channel.recv(200000)
                time.sleep(1)
                temp += resp
            return temp

    def db_ID_to_Value(self, itemID, list):
        # This function looks into a list of 2d tuples obtained from a dB and returns the element associated to its ID
        for item in list:
            if item[0] == itemID:
                return item[1].encode('utf-8')

    def display_general_info(self):
        self.macLabelValue.SetLabel(self.modemCommandOutputsDict['mac'])
        self.IPLabelValue.SetLabel(self.modemCommandOutputsDict['IP'])
        self.primaryChLabelValue.SetLabel(self.modemCommandOutputsDict['primary'])
        self.mdLabelValue.SetLabel(self.modemCommandOutputsDict['md'])
        self.sidLabelValue.SetLabel(self.modemCommandOutputsDict['sid'])
        self.mtcLabelValue.SetLabel(self.modemCommandOutputsDict['mtc'])
        self.usXdsLabelValue.SetLabel(self.modemCommandOutputsDict['dsXus'])
        self.USSFIDLabelValue.SetLabel(self.modemCommandOutputsDict['ussfid'])
        self.DSSFIDLabelValue.SetLabel(self.modemCommandOutputsDict['dssfid'])
        self.classifiersLabelValue.SetLabel(self.modemCommandOutputsDict['classifiers'])
        self.hostLabelValue.SetLabel(self.modemCommandOutputsDict['host'])
        self.vendorLabelValue.SetLabel(self.modemCommandOutputsDict['vendor'])
        self.modelLabelValue.SetLabel(self.modemCommandOutputsDict['model'])



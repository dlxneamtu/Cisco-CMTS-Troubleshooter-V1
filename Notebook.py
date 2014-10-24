__author__      = "Dan Neamtu"
__copyright__   = "Copyright 2014, Cisco Systems, Inc"
__credits__     = ["Dan Neamtu"]
__version__     = "1.0"
__status__      = "Development"

import wx
import wx.lib.scrolledpanel
import Intro
import ModemInfo
import ModemTroubleshooter
import ConfigurationReader

##########################################################################
## Class MainNotebook
## This is my Notebook class that will hold multiple tabs
###########################################################################

class Notebook(wx.Notebook):

    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, style=wx.NB_TOP)

        self.introTab = Intro.Intro(self)
        self.configurationReaderTab = ConfigurationReader.ConfigurationReader(self)
        self.modemInfoTab = ModemInfo.ModemInfo(self)
        self.troubleshooterTab = ModemTroubleshooter.ModemTroubleshooter(self)

        self.AddPage(self.introTab, "Intro")
        self.AddPage(self.configurationReaderTab, "Configuration Reader")
        self.AddPage(self.modemInfoTab, "Modem Information")
        self.AddPage(self.troubleshooterTab, "Health Check Audit")
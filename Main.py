__author__      = "Dan Neamtu"
__copyright__   = "Copyright 2014, Cisco Systems, Inc"
__credits__     = ["Dan Neamtu"]
__version__     = "1.0"
__status__      = "Development"

import wx
import wx.lib.scrolledpanel
import Notebook

##########################################################################
## Class MainFrame
## This will be the main frame which holds the menu and the notebook
###########################################################################

class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):

        x,y = wx.GetDisplaySize()
        wx.Frame.__init__(self, parent, id, title, size=(x-300, y-200))

        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(101, 'Quit', '' )
        menubar.Append(file, "&File")
        self.SetMenuBar(menubar)
        wx.EVT_MENU(self, 101, self.OnQuit)
        nb = Notebook.Notebook(self) # Adding the notebook to the frame. The Notebook will contain the rest
        self.StatusBar()

    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()

    def OnQuit(self, event):
        self.Close()


##########################################################################
## Class MyApp
###########################################################################

class MyApp(wx.App):
    def OnInit(self):
         frame = MainFrame(None, -1, 'notebook.py')
         frame.Show(True)
         frame.Centre()
         frame.Fit()
         return True

##########################################################################
## Main
###########################################################################

if __name__ == '__main__':
     app = MyApp(0)
     app.MainLoop()
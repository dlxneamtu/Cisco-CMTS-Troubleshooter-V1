__author__ = 'dneamtu'
import wx
##########################################################################
## Class Troubleshooter
## This is the Notebook tab that will be used for the modem info application function
###########################################################################

class ModemTroubleshooter(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)



        secVSizerLeft = wx.BoxSizer(wx.VERTICAL)
        secVSizerRight = wx.BoxSizer(wx.VERTICAL)
        mainHSizer = wx.BoxSizer(wx.HORIZONTAL)

        mainHSizer.Add(secVSizerLeft)
        mainHSizer.Add(secVSizerRight)

        self.SetSizer(mainHSizer) #Sizer is set on the panel

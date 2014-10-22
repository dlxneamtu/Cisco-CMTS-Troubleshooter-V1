__author__ = 'dneamtu'
import wx
import smtplib

##########################################################################
## Class Intro
## This is the Notebook tab that will be used for introduction
###########################################################################

class Intro(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        mainHSizer = wx.BoxSizer(wx.HORIZONTAL)
        secVSizerLeft = wx.BoxSizer(wx.VERTICAL)
        secVSizerRight = wx.BoxSizer(wx.VERTICAL)
        flexGridSizerRight = wx.FlexGridSizer(cols=2, vgap = 2, hgap=1)

        self.introText = wx.StaticText(self, -1, "Welcome to the CMTS Troubleshooter\n\n"
        "Features in version 1\n\n"
        "Parse a CMTS configuration and break it down into logical elements everything to be presented into graphical mode\n\n"
        "   Online mode - the configuration is extracted from CMTS via SSH\n\n"
        "   Offline mode - the configuration is loaded from a local configuration file \n\n"
        "The configuration elements that do not contain active configuration (that are not used)       are not displayed \n\n"
        "========================================================= \n\n"
        "Features/Functionalities to be added:\n\n"
        "On the 'CMTS Status' page go deeper into state of the system and provide more outputs (maybe graphically translated)\n\n"
        "On the 'CMTS Troubleshooter' page provide debugs and present an easy to read option for the debug session result\n\n"
        "On the 'Modem Troubleshooter' page get a modem MAC or IP address and provide complete info about it)",
        size=(600,600))

        self.feedbackText = wx.StaticText(self, -1, 'It would be great to hear from you! Leave me feedback below.')
        self.nameLabel = wx.StaticText(self, -1, 'Name')
        self.nameText = wx.TextCtrl(self, -1, size=(200,-1))
        self.orgLabel = wx.StaticText(self, -1, 'Organization')
        self.orgText = wx.TextCtrl(self, -1, size=(200,-1))
        self.emailLabel = wx.StaticText(self, -1, 'Email')
        self.emailText = wx.TextCtrl(self, -1, size=(200,-1))
        self.messageLabel = wx.StaticText(self, -1, 'Message')
        self.messageText = wx.TextCtrl(self, -1, size=(-1,-1),style=wx.TE_MULTILINE)
        self.okButton = wx.Button(self, -1, 'OK')
        self.emailSuccess = wx.StaticText(self, -1, '')


        flexGridSizerRight.Add(self.nameLabel)
        flexGridSizerRight.Add(self.nameText)
        flexGridSizerRight.Add(self.orgLabel)
        flexGridSizerRight.Add(self.orgText)
        flexGridSizerRight.Add(self.emailLabel)
        flexGridSizerRight.Add(self.emailText)
        flexGridSizerRight.Add(self.messageLabel)
        flexGridSizerRight.Add(self.messageText, flag=wx.EXPAND)
        flexGridSizerRight.Add(self.okButton)
        flexGridSizerRight.Add(self.emailSuccess)
        flexGridSizerRight.AddGrowableRow(3,1)
        flexGridSizerRight.AddGrowableCol(1,3)


        secVSizerLeft.Add(self.introText)
        secVSizerRight.Add(self.feedbackText)
        secVSizerRight.Add(wx.StaticText(self, -1, ''))
        secVSizerRight.Add(wx.StaticText(self, -1, ''))
        secVSizerRight.Add(flexGridSizerRight, proportion=1, flag=wx.EXPAND)

        mainHSizer.Add(secVSizerLeft)
        mainHSizer.Add(secVSizerRight, proportion=1, flag=wx.EXPAND)
        self.SetSizer(mainHSizer)

        self.okButton.Bind(wx.EVT_BUTTON, self.send_email)

    def send_email(self,e):

        server = smtplib.SMTP('smtp.gmail.com:587')

        #Next, log in to the server
        server.ehlo()
        server.starttls()
        server.login("dlxneamtu", "poko-0987")

        try:
            #Send the mail
            msg = "\n" + self.emailText.GetValue() # The /n separates the message from the headers
            msg = "\r\n".join([
                              "From: " + self.nameText.GetValue(),
                              "To: dlxneamtu@yahoo.com",
                              "Subject: CMTS Troubleshooter Feedback",
                              "",
                              "Organization: " + self.orgText.GetValue(),
                              "Email: " + self.emailText.GetValue(),
                              "Feedback: " + self.messageText.GetValue()
                              ])
            server.sendmail("dlxneamtu@gmail.com", "dlxneamtu@yahoo.com", msg)
            self.emailSuccess.SetLabel("Feedback successfully sent! Thank you!")

        except smtplib.SMTPException:
           print "Error: unable to send email"
__author__ = 'dneamtu'
import wx
from wx.lib.mixins.treemixin import VirtualTree
import sqlite3 as lite

##########################################################################
## Class ConfigTree
## This is the tree implementation from ConfigReader Notebook
###########################################################################

class ConfigTree(VirtualTree, wx.TreeCtrl):
    def __init__(self, *args, **kw):
        super(ConfigTree, self).__init__(*args, **kw)
        self.SetTreeElements()
        self.RefreshItems()


    def SetTreeElements(self):

        self.treeItems = []
        con = lite.connect('Cisco CMTS Troubleshooter Database.db')
        cur = con.cursor()

        with con:
            cur.execute("SELECT * FROM 'Tree Children Table'")
            self.childrenTable = cur.fetchall()

        with con:
            cur.execute("SELECT * FROM 'Tree Table'")
            while True:
                pair=(); tempChild = []
                row = cur.fetchone()

                if row == None:
                    break

                if row[2] == '':
                    pair += (row[1],[])
                else:
                    newRow = str(row[2]).replace(' , ',',').split(',')   # Row contained unicode u'11 , 12 , 13'
                    for childID in newRow:

                        tempChild.append((self.findChild(int(childID)),[]))
                    pair += (row[1],tempChild)
                self.treeItems.append(pair)

    def findChild(self, childId):
        for item in self.childrenTable:
            if item[0] == childId:
                return item[1]

    def GetTreeElements(self):
        result = []
        for item in self.treeItems:
            result.append(item[0])
            for subitem in item[1]:
                result.append(subitem[0])
        return result

    def UpdateTreeElements(self, string):
        for i in self.treeItems:
            if len(i[1]) != 0:
                for k in i[1]:
                    if k[0] == string:
                        index = i[1].index(k)
                        del i[1][index]
            else:
                if i[0] == string:
                    index = self.treeItems.index(i)
                    del self.treeItems[index]

    def OnGetItemText(self, index):
        return self.GetText(index)

    def OnGetChildrenCount(self, indices):
        return self.GetChildrenCount(indices)

    def GetItem(self, indices):
        text, children = 'Hidden root', self.treeItems
        for index in indices: text, children = children[index]
        return text, children

    def GetText(self, indices):
        return self.GetItem(indices)[0]

    def GetChildrenCount(self, indices):
        return len(self.GetChildren(indices))

    def GetChildren(self, indices):
        return self.GetItem(indices)[1]
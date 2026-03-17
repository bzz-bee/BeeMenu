#   BEEMENU  |  github.com/bzz-bee/BeeMenu
#       Author: Julius Schultz (bzz-bee)
#   Modify as you wish
#       Modified by: 

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from pathlib import Path
import subprocess
import sys

###    UI (Qt Designer)    ###
class Window(QFrame):
    def __init__(self):
        super().__init__()
    ### Window (self)
        self.setFixedSize(350, 500)
        font = QFont()
        font.setFamilies([u"Monospace"])
        font.setPointSize(10)
        self.setFont(font)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setLineWidth(2)
        self.setMidLineWidth(2)

    ### Left Side
        self.LeftSide = QFrame(self)
        self.LeftSide.setObjectName(u"LeftSide")
        self.LeftSide.setGeometry(QRect(8, 8, 224, 484))
        self.LeftSide.setFrameShape(QFrame.Shape.NoFrame)
        self.LeftSide.setFrameShadow(QFrame.Shadow.Sunken)
        self.LeftSide.setLineWidth(1)
        self.LeftSide.setMidLineWidth(1)

    ### App List UI
        self.AppList = QListWidget(self.LeftSide)
        self.AppList.setObjectName(u"AppList")
        self.AppList.setGeometry(QRect(0, 0, 224, 448))
        self.AppList.setFrameShape(QFrame.Shape.StyledPanel)
        self.AppList.setFrameShadow(QFrame.Shadow.Plain)
        self.AppList.setLineWidth(1)
        self.AppList.setMidLineWidth(1)
        self.AppList.setTabKeyNavigation(True)
        self.AppList.setIconSize(QSize(16, 16))
        self.AppList.setSpacing(4)
        self.AppList.setUniformItemSizes(True)
        
    ### Seach Bar UI
        self.SearchBar = QLineEdit(self.LeftSide)
        self.SearchBar.setObjectName(u"SearchBar")
        self.SearchBar.setGeometry(QRect(0, 456, 224, 28))
        self.SearchBar.setFrame(True)

    ### Right Side
        self.RightSide = QFrame(self)
        self.RightSide.setObjectName(u"RightSide")
        self.RightSide.setGeometry(QRect(240, 8, 102, 484))
        self.RightSide.setFrameShape(QFrame.Shape.NoFrame)
        self.RightSide.setFrameShadow(QFrame.Shadow.Sunken)
        self.RightSide.setLineWidth(2)
        self.RightSide.setMidLineWidth(2)

    ### Power Off Button
        self.PowerOffB = QPushButton(text="Power Off",parent=self.RightSide)
        self.PowerOffB.setObjectName(u"PowerOffB")
        self.PowerOffB.setGeometry(QRect(0, 456, 102, 28))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemShutdown))
        self.PowerOffB.setIcon(icon)

    ### Reboot Button
        self.RebootB = QPushButton(text="Reboot",parent=self.RightSide)
        self.RebootB.setObjectName(u"RebootB")
        self.RebootB.setGeometry(QRect(0, 428, 102, 28))
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemReboot))
        self.RebootB.setIcon(icon1)

    ### Suspend Button
        self.SuspendB = QPushButton(text="Suspend",parent=self.RightSide)
        self.SuspendB.setObjectName(u"SuspendB")
        self.SuspendB.setGeometry(QRect(0, 400, 102, 28))
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemLockScreen))
        self.SuspendB.setIcon(icon2)

    ### Log Out Button
        self.LogOutB = QPushButton(text="Log Out",parent=self.RightSide)
        self.LogOutB.setObjectName(u"LogOutB")
        self.LogOutB.setGeometry(QRect(0, 372, 102, 28))
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemLogOut))
        self.LogOutB.setIcon(icon3)

###   Functions    ###

### App List
    def initAppList(self):
        #   BeeMenu will show apps from these paths:
        path1 = Path('/usr/share/applications')
        path2 = Path.home() / "BeeMenu/applications"
        #Why doesn't "~/" or "$HOME/" work??
        filelist = []
        namelist = []
        commandlist = []
        appdict = {}

        print(f'- Retrieving apps & their run commands...')
        for file in path1.rglob('*.desktop'):
            filelist.append(file)
        #for file in path2.rglob('*.desktop'):
            #filelist.append(file)

        for file in filelist:
            openfile = open(file)
            filetext = openfile.readlines()

            #Get the app's name
            for line in filetext:
                if line.startswith("Name="):
                    nameline = line
                    appname = nameline.replace("Name=","").replace("\n","")
                    #Add it to the name list
                    namelist.append(appname)
                    break

            #Get the app's exec command
            for line in filetext:
                if line.startswith("Exec="):
                    execline = line
                    command = execline.replace("Exec=", "").replace(" %U","").replace(" %u","").replace(" %F","").replace(" %f","").replace("\n","")
                    #Add it to the command list
                    commandlist.append(command)
                    break

            appdict[appname] = command
        print(appdict)

        namelist.sort() #Alphabetical
        #Each app name in namelist becomes an item in QListWidget
        #Must be after 'appdict[appname] = command'
        self.AppList.addItems(namelist)
        print('- Apps added to app list.')

        def onClick(item):
            valueCommand = appdict.get(item.text(), command)
            print(valueCommand)
            self.close()
            subprocess.run(valueCommand)

        self.AppList.itemClicked.connect(onClick)

### Search Bar
    def initSearchBar(self):
        self.SearchBar.textChanged.connect(self.filter)
    def filter(self, text):
        for i in range(self.AppList.count()):
            item = self.AppList.item(i)
            if text.lower() == "" or item.text().lower().startswith(text.lower()):
                item.setHidden(False)
            else:
                item.setHidden(True)
    
### Buttons
    def initButtons(self):

        def poweroff(self):
            subprocess.call('sudo poweroff',shell=True)
        
        def reboot(self):
            subprocess.call('sudo reboot',shell=True)
       
        def suspend(self):
            subprocess.call('sudo systemctl suspend',shell=True)
        
        def logout(self):
            subprocess.call('logout',shell=True)

        self.PowerOffB.clicked.connect(poweroff)
        self.RebootB.clicked.connect(reboot)
        self.SuspendB.clicked.connect(suspend)
        self.LogOutB.clicked.connect(logout)


### Translate
    def retranslateUi(self, Window):
        self.retranslateUi(Window)
        QMetaObject.connectSlotsByName(self)
        self.SearchBar.setPlaceholderText(QCoreApplication.translate("Window", u"Search...", None))
        self.ShutDownB.setText(QCoreApplication.translate("Window", u"Shut Down", None))
        self.RebootB.setText(QCoreApplication.translate("Window", u"Reboot", None))
        self.SleepB.setText(QCoreApplication.translate("Window", u"Sleep", None))
        self.LogOutB.setText(QCoreApplication.translate("Window", u"Log Out", None))
        pass

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.initAppList()
    window.initSearchBar()
    window.initButtons()
    sys.exit(app.exec())
if __name__ == '__main__':
    main()

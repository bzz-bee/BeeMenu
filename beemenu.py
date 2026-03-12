
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6 import QtGui
from pathlib import Path
import subprocess
import sys
app = QApplication(sys.argv)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(250, 500))
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(20)
        

class Applist(Window):
    def __init__(self):
        super().__init__()
        applistW = QListWidget()
        path1 = Path('/usr/share/applications')
        path2 = Path('~/.local/share/applications')
        #path1 = Path('test_dir/test1')
        #path2 = Path('test_dir/test2')
        filelist = []
        namelist = []
        print(f'- Retrieving apps...')

        for file in path1.rglob('*.desktop'):
            filelist.append(file)
        for file in path2.rglob('*.desktop'):
            filelist.append(file)

        for file in filelist:
            openfile = open(file)
            filetext = openfile.readlines()

            #Get the app's name
            for line in filetext:
                if line.startswith("Name="):
                    nameline = line
                    appname = nameline.replace("Name=", "")
                    #Add it to the list
                    namelist.append(appname)
                    break
            #Get the app's exec command
            for line in filetext:
                if line.startswith("Exec="):
                    execline = line
                    command = execline.replace("Exec=", "")
                    break

        namelist.sort() #Alphabetical
        #Each app name in namelist becomes an item in QListWidget
        applistW.addItems(namelist)
        applistW.itemClicked.connect(applistW.itemClicked)
        print('- Apps added to QListWidget.')     

        def itemClicked(self,item):
            for item in self(command):
                print(command)
                subprocess.run(command)

def main(): 
    window = Window()
    window.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    main()

        

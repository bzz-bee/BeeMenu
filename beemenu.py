from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout
from PyQt6.QtCore import QSize
from PyQt6 import QtGui
from pathlib import Path
import subprocess
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(250, 500))
        self.initApplist()

    def initApplist(self):
        self.show()
        applistW = QListWidget()
        layout = QVBoxLayout()
        layout.addWidget(applistW)
        self.setLayout(layout)

        def onClick():
                print('Test')
                #for item in self(command):
                    #print(command)
                    #subprocess.run(command)

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
                    appname_noName = nameline.replace("Name=", "")
                    appname = appname_noName.replace("\n", "")
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
        applistW.itemClicked.connect(onClick)
        print('- Apps added to app list.')
        
        
        
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
if __name__ == '__main__':
    main()

        

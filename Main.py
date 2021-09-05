from PrimaryFunctions import *


def menu():
    clear()
    print("\n******************************************"
          "\n**\t\t  Befehle  \t\t**"
          "\n******************************************"
          "\n**\t(1)\tServer starten\t\t**"
          "\n**\t(2)\tDaten konvertieren\t**"
          "\n**\t(3)\tDaten speichern\t\t**"
          "\n**\t(4)\tBackup Assistent\t**"
          "\n**\t(X)\tBeenden\t\t\t**"
          "\n******************************************")
    takeInput()


def takeInput():
    selection = input("Befehl Auswählen: ")

    if selection == "1":
        startServer()

    elif selection == "2":
        convertRawData()

    elif selection == "3":
        safeDataToRemoteFile()

    elif selection == "4":
        backupAssistant()

    elif selection.lower() == "x":
        print("Programm wird beendet")
        sleep(2)
        exit(0)

    else:
        print("Diese Eingabe ist ungültig!")
        takeInput()
    input("Enter um fortzufahren")
    menu()


generateFiles()
menu()

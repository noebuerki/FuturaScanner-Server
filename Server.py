from MainFunctions import *

Running = True


# Ruft Funktion Eins auf
def callFunctionOne():
    print("Server wird gestartet")
    startServer()
    menu()


# Ruft Funktion Zwei auf
def callFunctionTwo():
    print("Rohdatenausgabe aufgerufen")
    printRawData()
    menu()


# Ruft Funktion Drei auf
def callFunctionThree():
    print("Datenkonvertierung aufgerufen")
    convertRawData()
    menu()


# Ruft Funktion Vier auf
def callFunctionFour():
    print("Datenspeicherung aufgerufen")
    safeDataToRemoteFile()
    menu()


# Ruft Funktion Fünf auf
def callFunctionFive():
    print("Datensicherung aufgerufen")
    backupAssistant()
    menu()


# Ruft Funktion Sechs auf
def callFunctionSix():
    print("Hilfe aufgerufen")
    showHelp()
    menu()


# Beendet das Program
def stopIt():
    global Running
    print("Programm wird beendet")
    Running = False
    sleep(2)
    exit(69)


# Gruss an Aleks
def creepy():
    sleep(3)
    print("\n\n\n\n\bHallo Alex...")
    sleep(3)
    print("\n\bDu bist zwar komisch...")
    sleep(3)
    print("\n\bAber trotzdem mag ich dich...")
    sleep(3)
    print("\n\bMit freundlichen Grüssen...")
    sleep(3)
    print("\n\bVon Herzen, dein Kevin...\n(☞ﾟヮﾟ)☞ ☜(ﾟヮﾟ☜)")
    sleep(5)
    print("( ͡• ͜ʖ ͡• )")
    sleep(0.1)
    menu()


# HaHa
def easterEgg():
    global tryScore
    global befehlsnummer
    print("\nYou F***ing Donkey! Get your Typing Skills Going!")
    sleep(10)
    print("\nTask Failed Successfully!\n")
    sleep(8)
    tryScore = 0
    menu()


# Wird aufgerufen wenn eingegebene Funktion nicht definiert
def functionNotDefined():
    global tryScore
    global befehlsnummer
    print("Diese Eingabe ist ungültig!")
    befehlsnummer = input("Befehl Auswählen: ")
    tryScore = tryScore + 1


# Zeigt das Menu
def menu():
    print("\n\t******************************************\n\t**\t\t  Befehle  \t\t**")
    print("\t******************************************")
    print("\t**\t(1)\tServer starten\t\t**\n\t**\t(2)\tRohdaten auslesen\t**")
    print("\t**\t(3)\tDaten konvertieren\t**")
    print("\t**\t(4)\tDaten speichern\t\t**")
    print("\t**\t(5)\tBackup Assistent\t**")
    print("\t**\t(6)\tManual\t\t\t**")
    print("\t**\t(X)\tBeenden\t\t\t**\n\t******************************************")
    inputMenu()


# Eingabe unter Menu
def inputMenu():
    global tryScore
    global befehlsnummer
    inputs = ["1", "2", "3", "4", "5", "6", "X", "x", "Baum", "baum"]
    exitEingabe = False
    befehlsnummer = input("Befehl Auswählen: ")
    while exitEingabe == False:
        if befehlsnummer not in inputs:
            if tryScore < 5:
                functionNotDefined()
            else:
                easterEgg()
        if befehlsnummer in inputs:
            if tryScore > 5:
                easterEgg()
        if befehlsnummer == "1":
            print("\n")
            callFunctionOne()
        if befehlsnummer == "2":
            print("\n")
            callFunctionTwo()
        if befehlsnummer == "3":
            print("\n")
            callFunctionThree()
        if befehlsnummer == "4":
            print("\n")
            callFunctionFour()
        if befehlsnummer == "5":
            print("\n")
            callFunctionFive()
        if befehlsnummer == "6":
            print("\n")
            callFunctionSix()
        if befehlsnummer == "X" or befehlsnummer == "x":
            stopIt()
        if befehlsnummer == "Baum" or befehlsnummer == "baum":
            creepy()


# Start
fileGenerator()
menu()

import socket
from SecondaryFunctions import *
from time import sleep
import os.path

tryScore = 0
inputsData = ["1", "2", "X", "x"]
Interrupt = False


# Generiert Ausgabefiles, wenn nicht vorhanden
def fileGenerator():
    if os.path.isdir("Daten") == False:
        os.mkdir("Daten")
    if os.path.isdir("Daten\Backup") == False:
        os.mkdir("Daten\Backup")
    if os.path.isdir("Daten\Backup\History") == False:
        os.mkdir("Daten\Backup\History")
    if os.path.isdir("Daten\Work") == False:
        os.mkdir("Daten\Work")
    if os.path.isfile("Daten\Raw.txt") == False:
        CreateRaw = open("Daten\Work\Raw.txt", "w+")
        CreateRaw.close()
    if os.path.isfile("Daten\Output.txt") == False:
        CreateFinal = open("Daten\Work\Output.txt", "w+")
        CreateFinal.close()


# Empfangen und speichern von Daten
def startServer():
    global Interrupt
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Öffnet Socket
    serverSocket.bind((socket.gethostbyname(socket.gethostname()), 9090))
    serverSocket.listen()
    serverSocket.settimeout(1)  # Socket Timeout, somit funktioniert Keyboardinterrupt
    print("Der Server ist erfolgreich auf der Ip " + str(socket.gethostbyname(socket.gethostname())) + " gestartet\nZum beenden: CTRL + C\n")
    while Interrupt == False:
        try:
            try:  # Daten empfangen
                (clientConnected, clientAddress) = serverSocket.accept()
                dataFromClient = clientConnected.recv(70000)  # Hier Grösse (MTU) anpassen
                rawData = dataFromClient.decode()
                if rawData == "100":
                    clientConnected.send("101".encode())
                    print("%s:%s hat die Verbindung getestet" % (clientAddress[0], clientAddress[1]))
                else:
                    clientConnected.send("200".encode())
                    print("%s:%s hat Daten übertragen" % (clientAddress[0], clientAddress[1]))
                    MyRawWriteFile = open("Daten\Work\Raw.txt", "a")  # Daten zwischenspeichern
                    MyRawWriteFile.write(rawData)
                    MyRawWriteFile.flush()
                    MyRawWriteFile.close()
            except socket.timeout:
                pass
        except KeyboardInterrupt:
            print("\nDer Server wird heruntergefahren")
            Interrupt = True
            break
    if Interrupt == True:  # Socket schliessen
        Interrupt = False
        serverSocket.close()
        sleep(2)
        print("\nDer Server wurde erfolgreich heruntergefahren")


# Ausgeben der Rohdaten
def printRawData():
    MyRawReadFile = open("Daten\Work\Raw.txt")
    for Line in MyRawReadFile:
        LineList = Line.split(";")
        FullNummerList = list(LineList[4])
        FullNummerList.remove("\n")
        Nummer = "".join(FullNummerList)
        print(LineList[0] + "\t" + LineList[1] + "\t" + LineList[2] + "\t" + LineList[3] + "\t" + Nummer)
    MyRawReadFile.close()
    sleep(2)
    print("\nDie Rohdaten wurden erfolgreich ausgegeben")


# Daten Konvertieren
def convertRawData():
    print("\nDaten werden konvertiert")
    global inputsconfirmation
    MyRawReadFile = open("Daten\Work\Raw.txt", "r")
    MyFinalWriteFile = open("Daten\Work\Output.txt", "a")
    Date = formatDate()
    Time = str(datetime.datetime.now().strftime("%H:%M:%S"))
    MyFinalWriteFile.write("RT00\n1\t\t" + Date + "\t" + Time + "\t2\nRT38\n")  # Schreibt Header ins File
    for line in MyRawReadFile:  # Schreibt Daten Linie für Linie
        combined = line.split(";")
        EAN = combined[0]
        Filiale = combined[1]
        Datum = combined[2]
        Block = combined[3]
        NummerWrong = combined[4]
        NummerWrongList = list(NummerWrong)
        NummerWrongList.remove("\n")
        Nummer = "".join(NummerWrongList)
        MyFinalWriteFile.write(
            EAN + "\t0\t" + Filiale + "\t" + Datum + "\t" + Block + "\t" + Nummer + "\t1,00\t0\t0\t\t0\t0\t0\t0\t0\n")
    MyFinalWriteFile.write("\n")  # Abschlussklausel
    MyFinalWriteFile.flush()
    MyRawReadFile.close()  # Alle Dateien schliessen
    MyFinalWriteFile.close()
    MyRawWriteFile = open("Daten\Work\Raw.txt", "w")
    MyRawWriteFile.write("")
    MyRawWriteFile.flush()
    MyRawWriteFile.close()
    sleep(2)
    print("\nDie Daten wurden erfolgreich konvertiert")


# Daten in eigenes File speichern
def safeDataToRemoteFile():
    MyFinalReadFile = open("Daten\Work\Output.txt", "r")
    transferData = MyFinalReadFile.read()
    MyFinalReadFile.close()
    nameRaw = input("Geben Sie den Namen der Zieldatei ein: ")
    exportFileHandler(nameRaw, transferData)


# Koordination Backup
def backupAssistant():
    global inputsData
    global tryScore
    # Menu ausgeben
    print("\n\t******************************************\n\t**\t\t  Befehle  \t\t**")
    print("\t******************************************")
    print("\t**\t(1)\tBackup erstellen\t**\n\t**\t(2)\tBackup wiederherstellen\t**")
    print("\t**\t(X)\tBeenden\t\t\t**\n\t******************************************")
    state = input("Befehl Auswählen: ")
    # Eingabe überprüfen
    if state not in inputsData:
        print("Diese Eingabe ist ungültig!")
    if state in inputsData:
        if state == "1":
            print("\nDas Backup wird erstellt\n")
            createBackup()
        if state == "2":
            success = restoreBackup()
            if success == False:
                backupAssistant()
        if state == "X" or state == "x":
            print("\nBackup abgebrochen!\n")
            sleep(2)


# Hilfe aufrufen
def showHelp():
    helpStartServer()
    helpPrintRawData()
    helpConvertData()
    helpSaveDataToRemoteFile()
    helpBackupHandler()
    input("\nDrücken Sie die \"Enter-Taste\" um diese Ansicht zu verlassen: ")
    system('cls')
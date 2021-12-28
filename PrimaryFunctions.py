import os.path
import socket
from os import system, name

from SecondaryFunctions import *


def generateFiles():
    if not os.path.isdir("data"):
        os.mkdir("data")

    if not os.path.isdir("data/backup"):
        os.mkdir("data/backup")

    if not os.path.isdir("data/backup/history"):
        os.mkdir("data/backup/history")

    if not os.path.isdir("data/cache"):
        os.mkdir("data/cache")

    if not os.path.isfile("data/cache/values.txt"):
        open("data/cache/values.txt", "w+").close()

    if not os.path.isfile("data/cache/output.txt"):
        open("data/cache/output.txt", "w+").close()


def startServer():
    print("\nDer Server wird gestartet...\n")

    interrupt = False

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((socket.gethostbyname(socket.gethostname()), 9090))
    serverSocket.listen()
    serverSocket.settimeout(1500)

    print("Der Server ist erfolgreich auf der Ip " + str(socket.gethostbyname(socket.gethostname())) + " gestartet"
                                                                                                       "\nZum beenden: CTRL + C\n")

    while not interrupt:
        try:
            try:
                (connectedClient, clientAddress) = serverSocket.accept()
                data = connectedClient.recv(14600).decode()

                if data == "ConnectionCheck-Request":
                    connectedClient.send("ConnectionCheck-Reply\n".encode())
                    connectedClient.close()
                else:
                    createBackup()
                    print("Backup erstellt")

                    deliveryFinished = False

                    data = ""
                    delivery = 0

                    while not deliveryFinished:
                        partialData = connectedClient.recv(14600).decode()

                        if partialData == "DeliveryReport":
                            connectedClient.send((str(delivery) + ";" + str(data.count("\n")) + "\n").encode())
                            connectedClient.close()
                            deliveryFinished = True
                            continue

                        delivery += 1
                        data += partialData
                        connectedClient.send(("Delivery:" + str(delivery) + "\n").encode())

                    valuesFile = open("data/cache/values.txt", "a")
                    valuesFile.write(data)
                    valuesFile.flush()
                    valuesFile.close()

                    print(str(data.count("\n")) + " Datensätze gespeichert")
            except socket.timeout:
                pass

        except KeyboardInterrupt:
            print("\nDer Server wird gestoppt")
            interrupt = True

    if interrupt:
        serverSocket.close()
        sleep(2)
        print("Der Server wurde erfolgreich gestoppt")


def convertRawData():

    createBackup()
    print("\nBackup erstellt")
    print("Daten werden konvertiert...")

    valuesFile = open("data/cache/values.txt", "r")

    if valuesFile.read() != "":
        valuesFile.seek(0)
        outputFile = open("data/cache/output.txt", "a")

        headerDate = formatDate()
        headerTime = str(datetime.datetime.now().strftime("%H:%M:%S"))

        outputFile.write("RT00\n1\t\t" + headerDate + "\t" + headerTime + "\t2\t\nRT38\n")

        for line in valuesFile:
            lineArray = line.split(";")
            numberArray = list(lineArray[4])
            numberArray.remove("\n")
            number = "".join(numberArray)
            outputFile.write(
                lineArray[0] + "\t0\t" + lineArray[1] + "\t" + lineArray[2] + "\t" + lineArray[
                    3] + "\t" + number + "\t1,00\t0\t0\t\t0\t0\t0\t0\t0\t\t\n")

        outputFile.write("\n")

        outputFile.flush()
        valuesFile.close()
        outputFile.close()

        valuesFile = open("data/cache/values.txt", "w")
        valuesFile.write("")

        valuesFile.flush()
        valuesFile.close()

    sleep(2)
    print("\nDie Daten wurden erfolgreich konvertiert")


def safeDataToRemoteFile():
    outputFile = open("data/cache/output.txt", "r")
    values = outputFile.read()
    outputFile.close()
    filename = input("\nGeben Sie den Namen der Zieldatei ein: ")

    if filename.endswith(".txt") or filename.endswith(".TXT"):
        name = filename
    else:
        name = filename + ".txt"

    location = input("Geben Sie bitte den vollständigen Pfad des Zielverzeichnisses an: ")

    if location.endswith("\\"):
        path = name
    else:
        path = "\\" + name

    if os.path.isfile(location + path):
        confirmation = input("Es werden alle bereits gespeicherten Daten Überschrieben! Trotzdem weiterfahren? [y/N]: ")

        while confirmation.lower() != "y" and confirmation != "" and confirmation.lower() != "n":
            print("Diese Eingabe ist ungültig!")
            confirmation = input(
                "Es werden alle bereits gespeicherten Daten Überschrieben! Trotzdem weiterfahren? [y/N] ")
        if confirmation == "":
            confirmation = "n"
    else:
        confirmation = "y"

    if confirmation.lower() == "y":
        if os.path.isdir(location):
            try:
                exportFile = open(location + path, "w+")
                exportFile.write(values)
                exportFile.flush()
                exportFile.close()
                sleep(2)
                print("\nDie Daten wurden erfolgreich in " + location + path + " gespeichert!")
            except Exception:
                sleep(2)
                print("\nDie Daten konnten nicht gespeichert werden, bitte überprüfen Sie Ihre Angaben!")
        else:
            sleep(2)
            print("\nDie Daten konnten nicht gespeichert werden, bitte überprüfen Sie Ihre Angaben!")
    elif confirmation.lower() == "n":
        sleep(2)
        print("\nDatenspeicherung abgebrochen!")


def backupAssistant():
    clear()
    print("\n******************************************"
          "\n**\t\t  Befehle  \t\t**"
          "\n******************************************"
          "\n**\t(1)\tBackup erstellen\t**"
          "\n**\t(2)\tBackup wiederherstellen\t**"
          "\n**\t(X)\tZurück\t\t\t**"
          "\n******************************************")
    selection = input("Befehl Auswählen: ")

    if selection == "1":
        print("\nDas Backup wird erstellt...\n")
        createBackup()
        print("Das Backup wurde erfolgeich erstellt")

    elif selection == "2":
        restoreBackup()

    elif selection.lower() == "x":
        return

    else:
        print("Diese Eingabe ist ungültig!")
        backupAssistant()


def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

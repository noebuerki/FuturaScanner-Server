import datetime
import os.path
import os.path
from os import system
from time import sleep

inputsconfirmation = ["Y", "y", "N", "n"]


# Speichert die Daten in ein neues File
def exportFileHandler(nameRaw, transferData):
    if nameRaw.endswith(".txt") or nameRaw.endswith(".TXT"):
        name = nameRaw
    else:
        name = nameRaw + ".txt"
    location = input("Geben Sie bitte den vollständigen Pfad des Zielverzeichnisses an: ")
    if location.endswith("\\"):
        path = name
    else:
        path = "\\" + name
    if os.path.isfile(location + path):
        confirmation = input("Es werden alle bereits gespeicherten Daten Überschrieben! Trotzdem weiterfahren? [Y/N] ")
    else:
        confirmation = "Y"
    if confirmation not in inputsconfirmation:
        print("Diese Eingabe ist ungültig!")
        confirmation = input("Es werden alle bereits gespeicherten Daten Überschrieben! Trotzdem weiterfahren? [Y/N] ")
    if confirmation in inputsconfirmation:
        if confirmation == "Y" or confirmation == "y":
            if os.path.isdir(location):
                try:
                    MyDestinationFile = open(location + path, "w+")
                    MyDestinationFile.write(transferData)
                    MyDestinationFile.flush()
                    MyDestinationFile.close()
                    sleep(2)
                    print("\nDie Daten wurden erfolgreich in " + location + path + " gespeichert!")
                except Exception:
                    sleep(2)
                    print("\nDie Daten konnten nicht gespeichert werden, bitte überprüfen Sie Ihre Angaben!")
            else:
                sleep(2)
                print("\nDie Daten konnten nicht gespeichert werden, bitte überprüfen Sie Ihre Angaben!")
        if confirmation == "N" or confirmation == "n":
            sleep(2)
            print("\nDatenspeicherung abgebrochen!")


# Konvertiert das Datum
def formatDate():
    DateUS = datetime.datetime.now()
    Date = DateUS.strftime("%d.%m.%Y")
    return Date


# Konvertiert das Datum für den Filenamen
def formatDateFileName():
    DateUS = datetime.datetime.now()
    Date = DateUS.strftime("%d-%m-%Y")
    return Date


# Konvertiert die Zeit für den Filenamen
def formatTime():
    import datetime
    TimeUS = datetime.datetime.now()
    Time = TimeUS.strftime("%H-%M")
    return Time


# Dateien erstellen, falls nicht vorhanden
def createBackup():
    Raw_Backup_File_Name = "Daten\Backup\Raw_Backup_" + formatDateFileName() + "_" + formatTime() + ".txt"
    MyRawBackup = open(Raw_Backup_File_Name, "w+")
    MyRawBackup.close()
    Output_Backup_File_Name = "Daten\Backup\Output_Backup_" + formatDateFileName() + "_" + formatTime() + ".txt"
    MyFinalBackup = open(Output_Backup_File_Name, "w+")
    MyFinalBackup.close()
    History_Backup_File_Name = formatDateFileName() + "_" + formatTime() + ".txt"
    MyHistory = open("Daten\Backup\History\\" + History_Backup_File_Name, "w+")
    MyHistory.close()
    # Daten kopieren
    MyRawBackupFile = open(Raw_Backup_File_Name, "w")
    MyFinalBackupFile = open(Output_Backup_File_Name, "w")
    MyRawReadFile = open("Daten\Work\Raw.txt")
    MyFinalReadFile = open("Daten\Work\Output.txt")
    MyRawData = MyRawReadFile.read()
    MyFinalData = MyFinalReadFile.read()
    MyRawBackupFile.write(MyRawData)
    MyFinalBackupFile.write(MyFinalData)
    MyRawBackupFile.flush()
    MyFinalBackupFile.flush()
    MyRawBackupFile.close()
    MyFinalBackupFile.close()
    sleep(2)


# Daten wiederherstellen
def restoreBackup():
    count = 1
    files = []
    print(" ")
    for file in os.listdir("Daten\Backup\History\\"):
        file = file.replace(".txt", "")
        files.append(file)
        print(count, file)
        count += 1
    Selector = int(input("Welches Backup (Zeitpunkt) soll wiederhergestellt werden (1 bis " + str(count - 1) + "): "))
    if Selector >= 1 and Selector <= count - 1:
        DateAndTime = files[Selector - 1]
        for file in os.listdir("Daten\Backup\\"):
            if DateAndTime in file:
                MyRawBackupFile = open("Daten\Backup\Raw_Backup_" + DateAndTime + ".txt")
                MyFinalBackupFile = open("Daten\Backup\Output_Backup_" + DateAndTime + ".txt")
                MyRawWriteFile = open("Daten\Work\Raw.txt", "w")
                MyFinalWriteFile = open("Daten\Work\Output.txt", "w")
                MyRawBackupData = MyRawBackupFile.read()
                MyFinalBackupData = MyFinalBackupFile.read()
                MyRawWriteFile.write(MyRawBackupData)
                MyFinalWriteFile.write(MyFinalBackupData)
                MyRawWriteFile.flush()
                MyFinalWriteFile.flush()
                MyRawWriteFile.close()
                MyFinalWriteFile.close()
                sleep(2)
                print("\nDas Backup wurde erfolgreich wiederhergestellt")
                return True
        print("\nEs konnte kein Backup wiederhergestellt werden")
        return False
    else:
        print("Diese Angabe ist falsch! Veruschen Sie es noch einmal.")
        system('cls')
        return False


def helpStartServer():
    print("Wie starte ich den Server?")
    print("\tUm den Server zu starten, wählen sie im Hauptmenu\n\tden Befehl mit der Nummer 1 (Server starten).")
    print("\tAnschliessend wird der Server gestartet und kann nun\n\tVerbindungen entgegennehmen. Dabei können")
    print("\tmaximal 2000 Zeilen auf einmal übertragen werden.")
    print("\tWenn Sie den Server herunterfahren möchten, drücken Sie\n\teinmal die Tastenkombination CTRL + C.")
    print("\tDanach wird der Server gestopt und Sie werden ins Menu weitergeleitet.")


def helpPrintRawData():
    print("\nWie gebe ich die unverarbeiteten Daten aus?")
    print("\tUm die unverarbeiteten Rohdaten auszugeben, wählen Sie\n\tden Befehl mit der Nummer 2 (Rohdaten Augeben).")
    print("\tDanach werden die unverarbeiteten Daten auf der Konsole ausgegeben.")
    print("\tKurz darauf werden Sie wieder ins Menu weitergeleitet.")


def helpConvertData():
    print("\nWie konvertiere ich die unverarbeiteten Daten?")
    print("\tUm die unverarbeiteten Daten zu konvertieren,\n\twählen Sie im Hauptmenu den Befehl mit der Nummer")
    print("\t3 (Daten konvertieren). Danch werden die Daten im Hintergrund\n\tkonvertiert und zwischengespeichert.")


def helpSaveDataToRemoteFile():
    print("\nWie speichere ich meine Daten in eine Exportdatei?")
    print(
        "\tUm Die konvertierten Daten in eine Exportdatei zu speichern,\n\twählen Sie im Hauptmenu den Befehl mit der Nummer")
    print(
        "\t4 (Daten Speichern). Danach müssen Sie den Namen  der Zieldatei\n\teingeben, und den absoluten Pfad zum Speicherort.")
    print("\tDanach werden die Daten in die angegebene Datei gespeichert und\n\tsind somit für Sie zugänglich.")


def helpBackupHandler():
    print("\nWie erstelle ich ein Backup meiner Daten?")
    print(
        "\tUm ein Backup Ihrer wertvollen Daten zu erstellen, wählen Sie\n\tim Hauptmenu den Befehl mit der Nummer 5 (Backupassistent).")
    print("\tDanach wählen Sie die Option 1 (Backup erstellen)\n\tum ein neues Backup anzulegen.")
    print("\n\nWie stelle ich meine Daten wieder her?")
    print(
        "\tUm eines der zuvor erstellten Backups wiederherzustellen, wählen Sie\n\tim Hauptmenu den Befehl mit der Nummer 5 (Backupassistent).")
    print("\tDanach wählen Sie die Option 2 (Backup wiederherstellen)\n\tum ein die Daten wiederherzustellen.")
    print(
        "\tIm darauffolgenden Menu können Sie den Zeitpunkt festlegen,\n\tvorausgesetzt Sie haben zu diesem Zeitpunkt ein Backup erstellt.")

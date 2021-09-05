import datetime
import os.path
from time import sleep


def formatDate():
    DateUS = datetime.datetime.now()
    Date = DateUS.strftime("%d.%m.%Y")
    return Date


def formatDateFileName():
    DateUS = datetime.datetime.now()
    Date = DateUS.strftime("%d-%m-%Y_%H-%M-%S")
    return Date


def formatTime():
    import datetime
    TimeUS = datetime.datetime.now()
    Time = TimeUS.strftime("%H-%M")
    return Time


def createBackup():
    valuesBackupFilename = "data/backup/values_backup_" + formatDateFileName() + ".txt"
    valuesBackupFile = open(valuesBackupFilename, "w+")
    valuesBackupFile.close()
    outputBackupFilename = "data/backup/output_backup_" + formatDateFileName() + ".txt"
    outputBackupFile = open(outputBackupFilename, "w+")
    outputBackupFile.close()
    historyFilename = formatDateFileName() + ".txt"
    historyFile = open("data/backup/history/" + historyFilename, "w+")
    historyFile.close()
    # Daten kopieren
    valuesBackupFile = open(valuesBackupFilename, "w")
    outputBackupFile = open(outputBackupFilename, "w")
    valuesFile = open("data/cache/values.txt")
    outputFile = open("data/cache/output.txt")
    values = valuesFile.read()
    output = outputFile.read()
    valuesBackupFile.write(values)
    outputBackupFile.write(output)
    valuesBackupFile.flush()
    outputBackupFile.flush()
    valuesBackupFile.close()
    outputBackupFile.close()
    sleep(2)


def restoreBackup():
    count = 1
    files = []
    print(" ")
    for file in os.listdir("data/backup/history/"):
        file = file.replace(".txt", "")
        files.append(file)
        print(count, file)
        count += 1
    selection = int(input("Welches Backup (Zeitpunkt) soll wiederhergestellt werden (1 bis " + str(count - 1) + "): "))
    if 1 <= selection <= count - 1:
        dateAndTime = files[selection - 1]

        valuesBackupFile = open("data/backup/values_backup_" + dateAndTime + ".txt")
        outputBackupFile = open("data/backup/output_backup_" + dateAndTime + ".txt")
        valuesFile = open("data/cache/values.txt", "w")
        outputFile = open("data/cache/output.txt", "w")
        valuesBackup = valuesBackupFile.read()
        outputBackup = outputBackupFile.read()
        valuesFile.write(valuesBackup)
        outputFile.write(outputBackup)
        valuesFile.flush()
        outputFile.flush()
        valuesFile.close()
        outputFile.close()
        sleep(2)
        print("\nDas Backup wurde erfolgreich wiederhergestellt")
        return True

    else:
        print("Diese Eingabe ist ungültig!")
        restoreBackup()

import os
import shutil
import subprocess
import platform
import json

platform = platform.system()
fileLoc = ""
fileDestinations = dict()

def getMacUser():
    command = "id -u -n"
    user = subprocess.check_output(command, shell = True, text = True)
    return user

def getFilePathDownloads():
    if platform == "Windows":
        fileNameDictWin()
        return "c:\\Users" + "\\" + os.getlogin() + "\\Downloads"
    elif platform == "Darwin":
        fileNameDictMac()
        return "/Users/" + getMacUser() + "/Downloads" 

def fileEnd(fileName, index, fileType):
    if fileName[index - 1] == '.':
        return fileType
    fileType = fileName[index - 1] + fileType
    return fileEnd(fileName, (index - 1), fileType)

def fileNameDictWin():
    windowsroot = "c:\\Users" + "\\" + os.getlogin()
    fileDestinations.update(dict.fromkeys(("zip", "7z", "rar", "zipx", "pkg"), windowsroot + r"\Documents\Downloads\Compressed"))
    fileDestinations.update(dict.fromkeys(("png", "jpg", "jpeg", "webp"), windowsroot + r"\Pictures\Downloads"))
    fileDestinations.update(dict.fromkeys(("docx", "pdf", "odt"), windowsroot + r"\Documents\Downloads\Docs\Docs"))
    fileDestinations.update(dict.fromkeys(("xlsx", "csv"), windowsroot + r"\Documents\Downloads\Docs\Excel"))
    fileDestinations.update(dict.fromkeys(["txt"], windowsroot + r"\Documents\Downloads\Docs\Txt"))
    fileDestinations.update(dict.fromkeys(["exe"], windowsroot + r"\Documents\Downloads\.exe"))

def fileNameDictMac():
    macroot = "/Users/" + getMacUser()
    fileDestinations.update(dict.fromkeys(["zip", "7z", "rar", "zipx", "pkg"], macroot + r"\Documents\Downloads\Compressed"))
    fileDestinations.update(dict.fromkeys(["png", "jpg", "jpeg", "webp"], macroot + r"\Pictures\Downloads"))
    fileDestinations.update(dict.fromkeys(["docx", "pdf", "odt"], macroot + r"\Documents\Downloads\Docs\Docs"))
    fileDestinations.update(dict.fromkeys(["xlsx", "csv"], macroot + r"\Documents\Downloads\Docs\Excel"))
    fileDestinations.update(dict.fromkeys(["txt"], macroot + r"\Documents\Downloads\Docs\Txt"))
    fileDestinations.update(dict.fromkeys(["exe"], macroot + r"\Documents\Downloads\.exe"))

def whereToSendWin(fileName):
    fileType = fileEnd(fileName, len(fileName), '')
    if fileType in fileDestinations:
        return fileDestinations[fileType]
    else:
        return "c:\\Users" + "\\" + os.getlogin() + r"\Documents\Downloads\Misc"

def whereToSendMac(fileName):
    fileType = fileEnd(fileName, len(fileName), '')
    if fileType in fileDestinations:
        return fileDestinations[fileType]
    else:
        return "/Users/" + getMacUser() + "/Documents/Misc"
    
fileDirDownloads = getFilePathDownloads()
downloads = os.listdir(fileDirDownloads)

if platform == "Windows":
    if len(downloads) != 0:
        fileLoc = fileDirDownloads + "\\" + downloads[0]
    for index, files in enumerate(downloads):
        fileLoc = fileDirDownloads + "\\" + downloads[index]
        shutil.move(fileLoc, whereToSendWin(downloads[index]))
elif platform == "Darwin":
    if len(downloads) != 0:
        fileLoc = fileDirDownloads + "/" + downloads[0]
    for index, files in enumerate(downloads):
        fileLoc = fileDirDownloads + "/" + downloads[index]
        subprocess.run(["mv", fileLoc, whereToSendMac(downloads[index])])
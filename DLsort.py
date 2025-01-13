import os
import shutil
import subprocess
import platform

fileLoc = ""
fileDestinations = dict()

# Finds name of current user on Mac platform
def getMacUser():
    command = "id -u -n"
    user = subprocess.check_output(command, shell = True, text = True)
    return user

# Finds the file path of the default downloads folder and creates a dictionary with file extension / locations pairs
def getFilePathDownloads():
    if platform.system() == "Windows":
        fileNameDictWin()
        return "c:\\Users" + "\\" + os.getlogin() + "\\Downloads"
    elif platform.system() == "Darwin":
        fileNameDictMac()
        return "/Users/" + getMacUser() + "/Downloads" 

# Finds file extension type by going backwards from the end of the file name
def fileEnd(fileName, index, fileType):
    if fileName[index - 1] == '.':
        return fileType
    fileType = fileName[index - 1] + fileType
    return fileEnd(fileName, (index - 1), fileType)

# Creates dictionary of file extension / file location pairs for Windows OS
def fileNameDictWin():
    windowsroot = "c:\\Users" + "\\" + os.getlogin()
    fileDestinations.update(dict.fromkeys(("zip", "7z", "rar", "zipx", "pkg"), windowsroot + r"\Documents\Downloads\Compressed"))
    fileDestinations.update(dict.fromkeys(("png", "jpg", "jpeg", "webp"), windowsroot + r"\Pictures\Downloads"))
    fileDestinations.update(dict.fromkeys(("docx", "pdf", "odt"), windowsroot + r"\Documents\Downloads\Docs\Docs"))
    fileDestinations.update(dict.fromkeys(("xlsx", "csv"), windowsroot + r"\Documents\Downloads\Docs\Excel"))
    fileDestinations.update(dict.fromkeys(["txt"], windowsroot + r"\Documents\Downloads\Docs\Txt"))
    fileDestinations.update(dict.fromkeys(["exe"], windowsroot + r"\Documents\Downloads\.exe"))

# Creates dictionary of file extension / file location pairs for Mac OS
def fileNameDictMac():
    macroot = "/Users/" + getMacUser()
    fileDestinations.update(dict.fromkeys(["zip", "7z", "rar", "zipx", "pkg"], macroot + r"\Documents\Downloads\Compressed"))
    fileDestinations.update(dict.fromkeys(["png", "jpg", "jpeg", "webp"], macroot + r"\Pictures\Downloads"))
    fileDestinations.update(dict.fromkeys(["docx", "pdf", "odt"], macroot + r"\Documents\Downloads\Docs\Docs"))
    fileDestinations.update(dict.fromkeys(["xlsx", "csv"], macroot + r"\Documents\Downloads\Docs\Excel"))
    fileDestinations.update(dict.fromkeys(["txt"], macroot + r"\Documents\Downloads\Docs\Txt"))
    fileDestinations.update(dict.fromkeys(["exe"], macroot + r"\Documents\Downloads\.exe"))

# Gets file location from extension using the dicitonary
def whereToSendWin(fileName):
    fileType = fileEnd(fileName, len(fileName), '')
    if fileType in fileDestinations:
        return fileDestinations[fileType]
    else:
        return "c:\\Users" + "\\" + os.getlogin() + r"\Documents\Downloads\Misc"

# Gets file location from extension using the dicitonary
def whereToSendMac(fileName):
    fileType = fileEnd(fileName, len(fileName), '')
    if fileType in fileDestinations:
        return fileDestinations[fileType]
    else:
        return "/Users/" + getMacUser() + "/Documents/Misc"
    
fileDirDownloads = getFilePathDownloads()
downloads = os.listdir(fileDirDownloads)

# Moves files accordingly
if platform.system() == "Windows":
    if len(downloads) != 0:
        fileLoc = fileDirDownloads + "\\" + downloads[0]
    for index, files in enumerate(downloads):
        fileLoc = fileDirDownloads + "\\" + downloads[index]
        shutil.move(fileLoc, whereToSendWin(downloads[index]))
elif platform.system() == "Darwin":
    if len(downloads) != 0:
        fileLoc = fileDirDownloads + "/" + downloads[0]
    for index, files in enumerate(downloads):
        fileLoc = fileDirDownloads + "/" + downloads[index]
        subprocess.run(["mv", fileLoc, whereToSendMac(downloads[index])])

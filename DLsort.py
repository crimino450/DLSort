import os
import shutil
import platform

fileLoc = ""
fileDestinations = dict()


# Finds the file path of the default downloads folder and creates a dictionary with file extension / locations pairs
def getFilePathDownloads():
    if platform.system() == "Windows":
        fileNameDictWin()
        return "c:\\Users" + "\\" + os.getlogin() + "\\Downloads"
    else:
        print("Wrong System")
        quit()

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

# Makes folder if folder does not exist for filepaths in dictionary
for path in fileDestinations.values():
    if not os.path.exists(path):
        os.makedirs(path)

# Gets file location from extension using the dicitonary
def whereToSendWin(fileName):
    fileType = fileEnd(fileName, len(fileName), '')
    if fileType in fileDestinations:
        return fileDestinations[fileType]
    else:
        misc = "c:\\Users" + "\\" + os.getlogin() + r"\Documents\Downloads\Misc"
        if not os.path.exists(misc):
            os.makedirs(misc)
        return misc
    
fileDirDownloads = getFilePathDownloads()
downloads = os.listdir(fileDirDownloads)

# Moves files accordingly
if len(downloads) != 0:
    fileLoc = fileDirDownloads + "\\" + downloads[0]
for index, files in enumerate(downloads):
    fileLoc = fileDirDownloads + "\\" + downloads[index]
    shutil.move(fileLoc, whereToSendWin(downloads[index]))

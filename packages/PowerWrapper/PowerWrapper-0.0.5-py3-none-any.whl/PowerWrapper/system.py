import os
import sys
import platform

systeminformation = platform.uname()


class System():
        """
        To be implemented: Function to allow programmer to ask a UAC prompt. Allowing them to run commands/functions as administrator. 
        The old one was badly implemented :(
        """


        # waits for developer to call variables, then provides the details to the developer
        # When called the variables run a functions by using the platform library, which then fetches the values and stores them in the variable.
        os = systeminformation.system
        computer_name = systeminformation.node
        os_version = systeminformation.release
        os_build = systeminformation.version
        cpu_architechture = systeminformation.machine
        processor = systeminformation.processor

        
        # Used to install external libraries
        def installDependancy(self, libraryName):
                os.system(f"pip install {libraryName}")
        # Used to create files
        def createFile(self, createFilepath):
            open(f"{createFilepath}", "x")
        # Used to rename/move files
        def moveFile(self, moveFilepath, newMovefilepath):
                os.rename(moveFilepath, newMovefilepath)
        # Used to delete files    
        def removeFile(self, remFilename):
            os.remove(remFilename)
        # Used to execute/run files
        def executeFile(self, execFilename):
            os.startfile(execFilename)
        """
        These functions below aren"t run with your program, instead they"ll be executed seperately.
        """
        # Used to run specified command in the shell
        def runCommand(self, command):
            os.system(command)
        # Used to run specified command in command prompt
        def runCommandprompt(self, command):
            os.system(f"cmd /k {command}")
        # Used to run specified command in powershell
        def runPowershell(self, command):
             os.system(f"powershell /k {command}")

        """
        Function to detect OS Type
        """

        def detectOS(self):
            if sys.platform.startswith("freebsd"):
                return "freebsd"
            elif sys.platform.startswith("emscripten"):
                return "emscripten"
            elif sys.platform.startswith("cygwin"):
                return "cygwin"
            elif sys.platform.startswith("win32"):
                return "win32"
            elif sys.platform.startswith("wasi"):
                return "wasi"
            elif sys.platform.startswith("aix"):
                 return "aix"
            elif sys.platform.startswith("darwin"):
                 return "darwin"
            else:
                 return "Couldn't fetch OS name/type"
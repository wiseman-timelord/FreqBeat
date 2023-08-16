Set UAC = CreateObject("Shell.Application") 
UAC.ShellExecute "install.bat", "", "", "runas", 1 

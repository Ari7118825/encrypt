Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell -command ""Expand-Archive -Force 'python.zip'""", 0, True
objShell.Run "run.bat", 0, False
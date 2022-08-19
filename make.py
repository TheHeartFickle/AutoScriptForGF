from os import system


version = '1.0.0'
if __name__ == '__main__':
    system("pyinstaller -Dw -i resource/kar98k.ico sample/main.py")
    system("del main.spec")
    system("rd /s/q build")
    system("rename dist AutoScriptGF")

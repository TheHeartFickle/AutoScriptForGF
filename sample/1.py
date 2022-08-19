import winshell
from pathlib import Path

desktop = Path(winshell.desktop())
miniconda_base = Path(
    winshell.folder('CSIDL_LOCAL_APPDATA')) / 'Continuum' / 'miniconda3'
win32_cmd = str(Path(winshell.folder('CSIDL_SYSTEM')) / 'cmd.exe')
icon = str(miniconda_base / "Menu" / "Iconleak-Atrous-Console.ico")

my_working = str(Path(winshell.folder('CSIDL_PERSONAL')) / "py_work")
link_filepath = str(desktop / "python_working.lnk")

arg_str = "/K " + str(miniconda_base / "Scripts" / "activate.bat") + " " + str(
    miniconda_base / "envs" / "work")

with winshell.shortcut(link_filepath) as link:
    link.path = win32_cmd
    link.description = "Python(work)"
    link.arguments = arg_str
    link.icon_location = (icon, 0)
    link.working_directory = my_working
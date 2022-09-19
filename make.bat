@echo off

pyinstaller -Dw -i resource/kar98k.ico src/main.py

move "dist/main" ""

del main.spec
rd /s/q build
rd /s/q dist

cd main

mkdir modules
mkdir resource
rename "main.exe" ".AutoScriptForGF.exe"

cd ..

xcopy "modules" "main/modules" /s/y
xcopy "resource" "main/resource" /s/y

rename main AutoScriptForGF
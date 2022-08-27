@echo off
@REM activate base
SET GenFolder=AutoScriptForGF
 
if exist %GenFolder% (
        rd /s/q %GenFolder%
    )

pyinstaller Pack.spec

move "dist/main" ""

rd /s/q build
rd /s/q dist

rename main AutoScriptForGF
@REM pause

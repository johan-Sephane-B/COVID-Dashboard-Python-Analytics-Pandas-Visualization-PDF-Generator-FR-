@echo off
echo Verification de la structure du projet COVID-19 Dashboard
echo.

set "OK_COUNT=0"
set "TOTAL_COUNT=0"

call :check_file "app.py"
call :check_dir "pages"
call :check_dir "scripts"
call :check_file "scripts\__init__.py"
call :check_file "scripts\data_loader.py"
call :check_file "scripts\data_cleaner.py"
call :check_file "scripts\visualizations.py"
call :check_file "scripts\report_generator.py"
call :check_dir "data"
call :check_dir "data\raw"
call :check_dir "data\processed"

echo.
echo Resume: %OK_COUNT%/%TOTAL_COUNT% fichiers/dossiers OK
if %OK_COUNT%==%TOTAL_COUNT% (
    echo.
    echo PARFAIT: Tous les fichiers necessaires sont presents!
    echo Le dashboard devrait fonctionner correctement.
) else (
    echo.
    echo ATTENTION: Certains fichiers sont manquants.
    echo Verifiez la structure du projet.
)
goto :eof

:check_file
set /a TOTAL_COUNT+=1
if exist %~1 (
    echo OK: %~1
    set /a OK_COUNT+=1
) else (
    echo MANQUANT: %~1
)
goto :eof

:check_dir
set /a TOTAL_COUNT+=1
if exist %~1 (
    echo OK: %~1\
    set /a OK_COUNT+=1
) else (
    echo MANQUANT: %~1\
)
goto :eof
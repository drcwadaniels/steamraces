set CONDAPATH=C:\ProgramData\Anaconda3
set ENVNAME=steamraces
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
python "E:/Code/steamraces/steamscraper.py" 
pause
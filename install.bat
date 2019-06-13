@echo off
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
choco install git.install -y
choco install miniconda3 --params="/InstallationType:JustMe /AddToPath:1 /RegisterPython:1" -y
call refreshenv
cd %homedrive%%homepath%/documents
git clone https://temp@github.com/TenteEEEE/quiche_pantie_patch.git
cd quiche_pantie_patch
conda install --file requirements.txt -y
echo Pantie patch setup is completed!!
pause

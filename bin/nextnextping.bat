
cd ..\nextnextping

pyinstaller --noconsole --noconfirm nextnextping.py --hidden-import=.

cd ..\bin

copy /y *.json ..\nextnextping\dist\nextnextping

python.exe ../nextnextping/nextnextping.py



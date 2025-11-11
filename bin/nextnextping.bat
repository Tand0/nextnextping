
cd ..\nextnextping

pyinstaller --noconsole --noconfirm nextnextping.py --hidden-import=.

cd ..\bin

copy /y *.json ..\nextnextping\dist\nextnextping

copy /y test.csv ..\nextnextping\dist\nextnextping

python.exe ../nextnextping/nextnextping.py



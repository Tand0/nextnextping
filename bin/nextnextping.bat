
cd ..\nextnextping

pyinstaller --noconsole --noconfirm nextnextping.py

cd ..\bin

copy /y *.ttl  ..\nextnextping\dist\nextnextping
copy /y *.json ..\nextnextping\dist\nextnextping

python.exe ../nextnextping/nextnextping.py



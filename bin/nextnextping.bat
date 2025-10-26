
cd ..\src

pyinstaller --noconsole --noconfirm nextnextping.py

cd ..\bin

copy /y *.ttl  ..\src\dist\nextnextping
copy /y *.json ..\src\dist\nextnextping

python.exe ../src/nextnextping.py



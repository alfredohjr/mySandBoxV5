git pull

pip install pywin32
pip install virtualenv

if not exist .env pause

if exist amb\ (
    echo amb exist
) else (
    virtualenv amb
)
call amb\scripts\activate

copy amb\Lib\site-packages\pywin32_system32\* amb\Lib\site-packages\win32\

amb\scripts\pip.exe install -r requeriments.txt
amb\scripts\python.exe manage.py migrate

python service.py install
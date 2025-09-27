python -m PyInstaller --onefile --add-data "assets;assets" --icon=assets/icon.ico --noconsole src/main.py
move "dist\main.exe" "dist\hocconfig.exe"
del src/__pycache__
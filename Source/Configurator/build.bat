python -m PyInstaller --onefile --add-data "assets;assets" --icon=assets/icon.ico --noconsole src/main.py --hidden-import=pillow --hidden-import=psutil --hidden-import=dearpygui --hidden-import=numpy --hidden-import=pathlib
move "dist\main.exe" "dist\hocconfig.exe"

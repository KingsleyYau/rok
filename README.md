# ROK-Bot
 rok助手(国服)
 
### Requirements
- python
  version >= 3.7

- software
  - ADB version 29.0.5-5949299 (1.0.41)
    Adb Platform Tools Download and Extract(See Important Notes) https://dl.google.com/android/repository/platform-tools_r31.0.3-windows.zip
  - tesseract
    Tesseract-OCR Installation https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0.20211201.exe
  - Bluestacks
    https://cdn3.bluestacks.com/downloads/windows/nxt/5.4.100.1026/0129e8eb74f84fc396a1500329365a09/BlueStacksMicroInstaller_5.4.100.1026_native.exe?filename=BlueStacksMicroInstaller_5.4.100.1026_native_5ffb0694218e1b99e7000bed6dcbe547_0.exe

- libraries
  - opencv-python
  - pytesseract
  - numpy
  - pillow
  - pure-python-adb
  - requests
  - requests-toolbelt
  
### Set Up

- Use following commands to install package into you **python** / **python virtual environment** (version 3.7)

  ```
  pip install -r requirements.txt

  ```

- Download **ADB** version 29.0.5-5949299 (1.0.41) (require for same version or you can change version in adb.py)

  - move all **adb** files under: **project folder/adb/**

- Download **tesseract** version v5.0.0-alpha.20201127 (no require for same version)

  - move all **tesseract** files under: **project folder/tesseract/**

- Use following command to run project

  ```
  python main.py
  ```
    
### Configurations
- Emulator resolution must be <u>**1280x720**</u>
- Emulator must **Enable** Android Debug Bridge (ADB)
- Game language must be <u>**Chinese**</u>
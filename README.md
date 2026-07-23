<div align="center">

# 🗑️ theZIPtrash

### Automatically remove garbage ZIP files from your PC

![License](https://img.shields.io/badge/license-MIT-purple?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.0.1-purple?style=flat-square)

---

*Detects ZIP files that have already been extracted and automatically moves them to a trash folder. Keep your folders clean effortlessly.*

</div>

---

## ✨ Features

| Feature | Description |
|:---|:---|
| 🔍 **Auto-detection** | Scans folders every N seconds and detects already-extracted ZIPs |
| 🗂️ **ZIP trash** | Garbage ZIPs are moved to a safe folder, not deleted |
| 🔔 **Notifications** | Native system alerts when a garbage ZIP is detected |
| ⚡ **Restore** | Restore any ZIP with a single click from the interface |
| 🧠 **Restore memory** | Restored ZIPs are never re-deleted automatically |
| 🎨 **Modern UI** | Dark theme with purple accents, clean and professional design |
| 🖥️ **System tray** | Runs in the background with a tray icon |
| 🔄 **Auto-start** | Option to start automatically with Windows |
| 🛠️ **Windows service** | Optionally installs as a system service |
| ⚙️ **Configuration** | Customizable folders, adjustable scan interval |

---

## 📸 Screenshots

<div align="center">

```
╔══════════════════════════════════════════════════╗
║  🗑️ theZIPtrash                                 ║
║                                                  ║
║  Garbage ZIPs detected and managed               ║
║                                                  ║
║  ┌────────────────────────────────────────────┐  ║
║  │ Name      │ Size    │ Date   │ Original    │  ║
║  ├───────────┼─────────┼────────┼─────────────┤  ║
║  │ Prueba.zip│ 3.2 MB  │ 23/07  │ Downloads   │  ║
║  │ App.zip   │ 15.7 MB │ 22/07  │ Desktop     │  ║
║  └────────────────────────────────────────────┘  ║
║                                                  ║
║  [Restore]  [X Delete]                           ║
║                                                  ║
║  Monitoring: Active  [Settings] [Delete all]     ║
║                                                  ║
║       Made by: ruvexdev-official with opencode   ║
╚══════════════════════════════════════════════════╝
```

</div>

---

## 🚀 Installation

### Option 1: Installer (.exe)

1. Download `theZIPtrash-installer.exe` from [Releases](https://github.com/ruvexdev-official/theZIPtrash/releases)
2. Run the installer as administrator
3. Follow the wizard steps
4. Done! theZIPtrash will run in the background

### Option 2: Installer (.msi)

1. Download `theZIPtrash.msi` from [Releases](https://github.com/ruvexdev-official/theZIPtrash/releases)
2. Run the installer
3. A desktop shortcut will be created

### Option 3: Run from source

```bash
# Clone the repository
git clone https://github.com/ruvexdev-official/theZIPtrash.git
cd theZIPtrash

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

---

## 🛠️ Building

### Prerequisites

- Python 3.8+
- [NSIS](https://nsis.sourceforge.io/) (for .exe installer)
- [WiX Toolset v7](https://wixtoolset.org/) (for .msi installer)

### Generate executables

```bash
python build.py
```

Executables will be generated in the `dist/` folder.

### Generate NSIS installer

```bash
cd installer
makensis theZIPtrash.nsi
```

### Generate MSI installer

```bash
cd installer
wix build theZIPtrash.wxs -d DistDir=..\dist -d ProjectDir=.. -o theZIPtrash.msi -acceptEula wix7
```

---

## ⚙️ Configuration

Configuration is stored in:

```
%APPDATA%\theZIPtrash\config.json
```

### Configuration structure

```json
{
    "watched_folders": [
        "C:\\Users\\YourUser\\Downloads",
        "C:\\Users\\YourUser\\Desktop"
    ],
    "scan_interval": 10,
    "auto_start": false,
    "monitoring_paused": false,
    "deleted_zips": [],
    "ignored_zips": []
}
```

### Default monitored folders

| Folder | Location |
|:---|:---|
| 📥 Downloads | `C:\Users\{user}\Downloads` |
| 🖥️ Desktop | `C:\Users\{user}\Desktop` |

You can add or remove folders from **Settings** in the UI.

---

## 🏗️ Architecture

```
theZIPtrash/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── build.py                 # Build script
├── assets/
│   └── icon.ico             # Application icon
├── src/
│   ├── app.py               # Main orchestrator
│   ├── config.py            # Configuration management
│   ├── watcher.py           # Monitoring thread (QThread)
│   ├── zipper.py            # Move/restore ZIP logic
│   ├── notifications.py     # Native notifications (plyer)
│   ├── tray.py              # System tray icon
│   ├── autostart.py         # Windows auto-start
│   ├── service.py           # Windows service
│   └── ui/
│       ├── main_window.py   # Main window
│       ├── settings_dialog.py # Settings dialog
│       └── styles.py        # Dark/purple theme (QSS)
└── installer/
    ├── theZIPtrash.nsi      # NSIS script
    └── theZIPtrash.wxs      # WiX script
```

---

## 📋 Windows Service

theZIPtrash can run as a Windows service in the background without a GUI.

### Install service

```bash
dist\theZIPtrash-service.exe install
net start theZIPtrash
```

### Uninstall service

```bash
net stop theZIPtrash
dist\theZIPtrash-service.exe remove
```

---

## 🔧 Dependencies

| Package | Version | Usage |
|:---|:---|:---|
| [PyQt5](https://pypi.org/project/PyQt5/) | >=5.15 | GUI framework |
| [plyer](https://pypi.org/project/plyer/) | >=2.1 | Native notifications |
| [pywin32](https://pypi.org/project/pywin32/) | >=306 | Windows service, auto-start |

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License - Copyright (c) 2026 ruvexdev-official
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## 🐛 Reporting Bugs

If you find a bug, please [open an issue](https://github.com/ruvexdev-official/theZIPtrash/issues) with:

- Description of the problem
- Steps to reproduce
- Operating system version
- Python version

---

<div align="center">

**Made with 💜 by [ruvexdev-official](https://github.com/ruvexdev-official)**

</div>

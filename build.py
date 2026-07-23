import os
import subprocess
import sys
import shutil

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(ROOT_DIR, "dist")
BUILD_DIR = os.path.join(ROOT_DIR, "build")
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")


def clean():
    print("Cleaning previous builds...")
    for d in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(d):
            shutil.rmtree(d)
    for f in os.listdir(ROOT_DIR):
        if f.endswith(".spec"):
            os.remove(os.path.join(ROOT_DIR, f))
    print("Clean done.")


def build_gui():
    print("Building GUI executable...")
    icon_arg = ""
    icon_path = os.path.join(ASSETS_DIR, "icon.ico")
    if os.path.exists(icon_path):
        icon_arg = f"--icon={icon_path}"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--noconsole",
        "--onefile",
        icon_arg,
        "--name=theZIPtrash",
        "--add-data=assets;assets" if sys.platform == "win32" else "--add-data=assets:assets",
        "--hidden-import=plyer.platforms.win.notification",
        "--hidden-import=PyQt5.sip",
        os.path.join(ROOT_DIR, "main.py"),
    ]
    cmd = [c for c in cmd if c]
    subprocess.run(cmd, check=True)
    print(f"GUI build done: {os.path.join(DIST_DIR, 'theZIPtrash.exe')}")


def build_service():
    print("Building service executable...")
    icon_arg = ""
    icon_path = os.path.join(ASSETS_DIR, "icon.ico")
    if os.path.exists(icon_path):
        icon_arg = f"--icon={icon_path}"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--console",
        "--onefile",
        icon_arg,
        "--name=theZIPtrash-service",
        "--hidden-import=plyer.platforms.win.notification",
        "--hidden-import=win32service",
        "--hidden-import=win32serviceutil",
        "--hidden-import=win32event",
        "--hidden-import=servicemanager",
        os.path.join(ROOT_DIR, "src", "service.py"),
    ]
    cmd = [c for c in cmd if c]
    subprocess.run(cmd, check=True)
    print(f"Service build done: {os.path.join(DIST_DIR, 'theZIPtrash-service.exe')}")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
        return

    clean()
    build_gui()
    build_service()
    print("\nAll builds completed successfully!")
    print(f"Output directory: {DIST_DIR}")


if __name__ == "__main__":
    main()

import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

APP_NAME = "theZIPtrash"
REG_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_available():
    return sys.platform == "win32"


def is_enabled():
    if not is_available():
        return False
    try:
        import winreg

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_READ)
        try:
            winreg.QueryValueEx(key, APP_NAME)
            return True
        except FileNotFoundError:
            return False
        finally:
            winreg.CloseKey(key)
    except Exception as e:
        logger.warning(f"Error checking autostart: {e}")
        return False


def enable():
    if not is_available():
        return False
    try:
        import winreg

        exe_path = _get_executable_path()
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        logger.info(f"Autostart enabled: {exe_path}")
        return True
    except Exception as e:
        logger.error(f"Error enabling autostart: {e}")
        return False


def disable():
    if not is_available():
        return False
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_SET_VALUE
        )
        try:
            winreg.DeleteValue(key, APP_NAME)
        except FileNotFoundError:
            pass
        winreg.CloseKey(key)
        logger.info("Autostart disabled")
        return True
    except Exception as e:
        logger.error(f"Error disabling autostart: {e}")
        return False


def _get_executable_path():
    if getattr(sys, "frozen", False):
        return sys.executable
    return f'"{sys.executable}" "{Path(__file__).resolve().parent.parent.parent / "main.py"}"'

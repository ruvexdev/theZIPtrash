<div align="center">

# 🗑️ theZIPtrash

### Elimina automaticamente los ZIPs basura de tu PC

![License](https://img.shields.io/badge/license-MIT-purple?style=flat-square)
![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.0.1-purple?style=flat-square)

---

*Detecta ZIPs que ya han sido extraidos y los mueve automaticamente a una papelera. Mantene tus carpetas limpias sin esfuerzo.*

</div>

---

## ✨ Caracteristicas

| Caracteristica | Descripcion |
|:---|:---|
| 🔍 **Deteccion automatica** | Escanea carpetas cada N segundos y detecta ZIPs ya extraidos |
| 🗂️ **Papelera de ZIPs** | Los ZIPs "basura" se mueven a una carpeta segura, no se borran |
| 🔔 **Notificaciones** | Alertas nativas del sistema cuando se detecta un ZIP basura |
| ⚡ **Restauracion** | Restaura cualquier ZIP con un solo clic desde la interfaz |
| 🧠 **Memoria de restauracion** | Los ZIPs restaurados no se vuelven a borrar automaticamente |
| 🎨 **UI moderna** | Tema oscuro con acentos morados, diseno limpio y profesional |
| 🖥️ **System tray** | Se ejecuta en segundo plano con icono en la bandeja del sistema |
| 🔄 **Auto-start** | Opcion de iniciar automaticamente con Windows |
| 🛠️ **Servicio Windows** | Opcionalmente se instala como servicio del sistema |
| ⚙️ **Configuracion** | Carpetas personalizables, intervalo de escaneo ajustable |

---

## 📸 Capturas

<div align="center">

```
╔══════════════════════════════════════════════════╗
║  🗑️ theZIPtrash                                 ║
║                                                  ║
║  ZIPs basura detectados y gestionados            ║
║                                                  ║
║  ┌────────────────────────────────────────────┐  ║
║  │ Nombre    │ Tamano  │ Fecha  │ Original    │  ║
║  ├───────────┼─────────┼────────┼─────────────┤  ║
║  │ Prueba.zip│ 3.2 MB  │ 23/07  │ Downloads   │  ║
║  │ App.zip   │ 15.7 MB │ 22/07  │ Desktop     │  ║
║  └────────────────────────────────────────────┘  ║
║                                                  ║
║  [Restaurar]  [X Eliminar]                       ║
║                                                  ║
║  Monitoreo: Activo    [Config] [Eliminar todo]   ║
║                                                  ║
║       Made by: ruvexdev-official with opencode   ║
╚══════════════════════════════════════════════════╝
```

</div>

---

## 🚀 Instalacion

### Opcion 1: Instalador (.exe)

1. Descarga `theZIPtrash-installer.exe` desde [Releases](https://github.com/ruvexdev-official/theZIPtrash/releases)
2. Ejecuta el instalador como administrador
3. Sigue los pasos del asistente
4. ¡Listo! theZIPtrash se ejecutara en segundo plano

### Opcion 2: Instalador (.msi)

1. Descarga `theZIPtrash.msi` desde [Releases](https://github.com/ruvexdev-official/theZIPtrash/releases)
2. Ejecuta el instalador
3. Se creara un acceso directo en el escritorio

### Opcion 3: Ejecutar desde codigo fuente

```bash
# Clonar el repositorio
git clone https://github.com/ruvexdev-official/theZIPtrash.git
cd theZIPtrash

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

---

## 🛠️ Compilacion

### Requisitos previos

- Python 3.8+
- [NSIS](https://nsis.sourceforge.io/) (para instalador .exe)
- [WiX Toolset v7](https://wixtoolset.org/) (para instalador .msi)

### Generar ejecutables

```bash
python build.py
```

Los ejecutables se generaran en la carpeta `dist/`.

### Generar instalador NSIS

```bash
cd installer
makensis theZIPtrash.nsi
```

### Generar instalador MSI

```bash
cd installer
wix build theZIPtrash.wxs -d DistDir=..\dist -d ProjectDir=.. -o theZIPtrash.msi -acceptEula wix7
```

---

## ⚙️ Configuracion

La configuracion se almacena en:

```
%APPDATA%\theZIPtrash\config.json
```

### Estructura de configuracion

```json
{
    "watched_folders": [
        "C:\\Users\\TuUsuario\\Downloads",
        "C:\\Users\\TuUsuario\\Desktop"
    ],
    "scan_interval": 10,
    "auto_start": false,
    "monitoring_paused": false,
    "deleted_zips": [],
    "ignored_zips": []
}
```

### Carpetas monitoreadas por defecto

| Carpeta | Ubicacion |
|:---|:---|
| 📥 Descargas | `C:\Users\{user}\Downloads` |
| 🖥️ Escritorio | `C:\Users\{user}\Desktop` |

Puedes agregar o quitar carpetas desde **Configuracion** en la UI.

---

## 🏗️ Arquitectura

```
theZIPtrash/
├── main.py                  # Punto de entrada
├── requirements.txt         # Dependencias
├── build.py                 # Script de compilacion
├── assets/
│   └── icon.ico             # Icono de la aplicacion
├── src/
│   ├── app.py               # Orquestador principal
│   ├── config.py            # Gestion de configuracion
│   ├── watcher.py           # Hilo de monitoreo (QThread)
│   ├── zipper.py            # Logica de mover/restaurar ZIPs
│   ├── notifications.py     # Notificaciones nativas (plyer)
│   ├── tray.py              # Icono de bandeja del sistema
│   ├── autostart.py         # Inicio automatico con Windows
│   ├── service.py           # Servicio de Windows
│   └── ui/
│       ├── main_window.py   # Ventana principal
│       ├── settings_dialog.py # Dialogo de configuracion
│       └── styles.py        # Tema oscuro/morado (QSS)
└── installer/
    ├── theZIPtrash.nsi      # Script NSIS
    └── theZIPtrash.wxs      # Script WiX
```

---

## 📋 Servicio de Windows

theZIPtrash puede ejecutarse como servicio de Windows en segundo plano sin necesidad de interfaz grafica.

### Instalar servicio

```bash
dist\theZIPtrash-service.exe install
net start theZIPtrash
```

### Desinstalar servicio

```bash
net stop theZIPtrash
dist\theZIPtrash-service.exe remove
```

---

## 🔧 Dependencias

| Paquete | Version | Uso |
|:---|:---|:---|
| [PyQt5](https://pypi.org/project/PyQt5/) | >=5.15 | Interfaz grafica |
| [plyer](https://pypi.org/project/plyer/) | >=2.1 | Notificaciones nativas |
| [pywin32](https://pypi.org/project/pywin32/) | >=306 | Servicio de Windows, auto-start |

---

## 📜 Licencia

Este proyecto esta licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para mas detalles.

```
MIT License - Copyright (c) 2026 ruvexdev-official
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas!

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Haz commit de tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 🐛 Reportar errores

Si encuentras un bug, por favor [abre un issue](https://github.com/ruvexdev-official/theZIPtrash/issues) con:

- Descripcion del problema
- Pasos para reproducirlo
- Version del sistema operativo
- Version de Python

---

<div align="center">

**Hecho con 💜 por [ruvexdev-official](https://github.com/ruvexdev-official)**

</div>

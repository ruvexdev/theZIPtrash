; theZIPtrash NSIS Installer Script
; Requires NSIS (https://nsis.sourceforge.io/)

!include "MUI2.nsh"
!include "FileFunc.nsh"

Name "theZIPtrash"
OutFile "theZIPtrash-installer.exe"
InstallDir "$PROGRAMFILES\theZIPtrash"
RequestExecutionLevel admin

!define MUI_ICON "assets\icon.ico"
!define MUI_UNICON "assets\icon.ico"
!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TITLE "Bienvenido al asistente de instalacion de theZIPtrash"
!define MUI_WELCOMEPAGE_TEXT "Este asistente le guiará en la instalacion de theZIPtrash.$\r$\n$\r$\ntheZIPtrash detecta automaticamente los ZIPs que ya han sido extraidos y los mueve a una carpeta de papelera para mantener sus carpetas limpias.$\r$\n$\r$\nHaga clic en Siguiente para continuar."

!define MUI_FINISHPAGE_RUN "$INSTDIR\theZIPtrash.exe"
!define MUI_FINISHPAGE_RUN_TEXT "Ejecutar theZIPtrash"

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "Spanish"

Section "theZIPtrash (Principal)" SecMain
    SetOutPath "$INSTDIR"

    File "dist\theZIPtrash.exe"
    File "dist\theZIPtrash-service.exe"
    File "LICENSE"

    CreateDirectory "$APPDATA\theZIPtrash"
    CreateDirectory "$APPDATA\theZIPtrash\trash"

    CreateShortCut "$DESKTOP\theZIPtrash.lnk" "$INSTDIR\theZIPtrash.exe" "" "$INSTDIR\theZIPtrash.exe"

    CreateDirectory "$SMPROGRAMS\theZIPtrash"
    CreateShortCut "$SMPROGRAMS\theZIPtrash\theZIPtrash.lnk" "$INSTDIR\theZIPtrash.exe"
    CreateShortCut "$SMPROGRAMS\theZIPtrash\Desinstalar.lnk" "$INSTDIR\uninstall.exe"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\theZIPtrash" \
        "DisplayName" "theZIPtrash"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\theZIPtrash" \
        "UninstallString" '"$INSTDIR\uninstall.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\theZIPtrash" \
        "DisplayIcon" '"$INSTDIR\theZIPtrash.exe"'
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\theZIPtrash" \
        "Publisher" "ruvexdev-official"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\theZIPtrash" \
        "DisplayVersion" "1.0.0"

    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
SectionEnd

Section "Servicio de Windows" SecService
    DetailPrint "Instalando servicio de Windows..."
    ExecWait '"$INSTDIR\theZIPtrash-service.exe" install'
    ExecWait 'net start theZIPtrash'
SectionEnd

Section "Uninstall"
    ExecWait 'net stop theZIPtrash'
    ExecWait '"$INSTDIR\theZIPtrash-service.exe" remove"

    Delete "$DESKTOP\theZIPtrash.lnk"
    RMDir /r "$SMPROGRAMS\theZIPtrash"
    RMDir /r "$INSTDIR"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\theZIPtrash"
SectionEnd

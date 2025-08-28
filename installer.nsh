;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;Defines
  !define NAME "excelmaplink"
  !define APPFILE "excelmaplink.exe"
  !ifndef VERSION
    !define VERSION "UNKNOWN"
  !endif
  !define SLUG "${NAME} v${VERSION}"

;--------------------------------
;General

  ;Name and file
  Name "${NAME}"
  OutFile "${NAME}-setup.exe"
  Unicode True

  ;Default installation folder
  InstallDir "$LOCALAPPDATA\Programs\${NAME}"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\${NAME}" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel user

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING
  !define MUI_WELCOMEPAGE_TITLE "${SLUG} Installation"

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY

  ;start menu page config
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${NAME}"
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  
  Var StartMenuFolder
  !insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "German"

;--------------------------------
;Installer Sections

Section "-hidden Installation" 

  SetOutPath "$INSTDIR"
  
  File /r dist\excelmaplink\*.*
  
  ;Store installation folder
  WriteRegStr HKCU "Software\${NAME}" "" $INSTDIR
  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\${NAME}.lnk" "$INSTDIR\${APPFILE}"
    CreateShortcut "$SMPROGRAMS\$StartMenuFolder\${NAME} - Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  !insertmacro MUI_STARTMENU_WRITE_END

SectionEnd

;--------------------------------
;Uninstaller Section

Section "un.Uninstall"


  Delete "$INSTDIR\Uninstall.exe"

  RMDir /r "$INSTDIR"

  !insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder

  RMDir /r "$SMPROGRAMS\$StartMenuFolder"

  DeleteRegKey /ifempty HKCU "Software\${NAME}"

SectionEnd
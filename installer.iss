#define MyAppName "Password Manager"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Hamza Nahhas"
#define MyAppExeName "password_manager.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-47A8-91AB-1234567890CD}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=PasswordManagerSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=dist\password_manager\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons"; Flags: unchecked

[Files]
Source: "dist\password_manager\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent
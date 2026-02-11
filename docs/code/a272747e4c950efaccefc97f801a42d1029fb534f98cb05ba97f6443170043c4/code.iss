; -- Example1.iss --
; Demonstrates copying 3 files and creating an icon.

[Setup]
AppName=My Program
AppVersion=1.5
;AppVerName=My Program 1.5
AppPublisher=My Company, Inc.
;AppPublisherURL=http://www.example.com
;AppSupportURL=http://www.example.com
;AppUpdatesURL=http://www.example.com
DefaultDirName={pf}\My Program
DefaultGroupName=My Program
AllowNoIcons=yes
LicenseFile=license.rtf
InfoBeforeFile=readme.txt
OutputDir=userdocs:Inno Setup Example Scripts\Output
OutputBaseFilename=setup
Compression=lzma/fast
SolidCompression=yes

[Languages]
Name: en; MessagesFile: compiler:Default.isl

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked

[Files]
Source: "MyProg.exe"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: The icon will not be installed until the program is run
Source: "MyProg.chm"; DestDir: "{app}"; Flags: recursesubdirs
Source: "images\*"; DestDir: "{app}\images"; Flags: recursesubdirs

[Icons]
Name: "{group}\My Program"; Filename: "{app}\MyProg.exe"
Name: "{group}\{cm:UninstallProgram,My Program}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\My Program"; Filename: "{app}\MyProg.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\MyProg.exe"; Description: "{cm:LaunchProgram,My Program}"; Flags: nowait postinstall skipifsilent
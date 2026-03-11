[Setup]
AppName=My Program
AppVersion=1.0
DefaultDirName={pf}\My Program
DefaultGroupName=My Program
OutputBaseFilename=setup

[Files]
Source: "MyProg.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\My Program"; Filename: "{app}\MyProg.exe"
Name: "{group}\Uninstall My Program"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\MyProg.exe"; Description: "Launch My Program"; Flags: postinstall nowait

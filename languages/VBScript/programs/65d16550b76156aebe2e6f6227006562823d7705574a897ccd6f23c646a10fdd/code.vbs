Dim fso, file
Set fso = CreateObject("Scripting.FileSystemObject")
Set file = fso.CreateTextFile("c:\\testfile.txt", True)
file.WriteLine("This is a test.")
file.Close
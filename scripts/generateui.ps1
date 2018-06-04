Get-ChildItem "design" -Filter *.ui | 
Foreach-Object {
    Invoke-Expression "pyuic5 ..\design\$($_.BaseName).ui 2>&1" | Out-File "..\design\$($_.BaseName)_ui.py" -Encoding oem
}

mkdir --parents ../PrinterClient.AppDir/usr/bin
cp -r ../dist/main/* ../PrinterClient.AppDir/usr/bin

cat << 'EOF' >> ../PrinterClient.AppDir/AppRun
#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
exec "$HERE/usr/bin/main"
EOF

cat << 'EOF' >> ../PrinterClient.AppDir/printerclient.desktop
[Desktop Entry]
Name=PrinterClient
Exec=main
Icon=icon
Type=Application
Categories=Utility;
EOF

cp icon.png ../PrinterClient.AppDir/icon.png

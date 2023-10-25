#!/bin/bash
# start services
echo "iniciando servicio"
service dbus start
service bluetooth start
echo "BT iniciado"
# start application
python3 aplicacion.py
echo "app iniciada"

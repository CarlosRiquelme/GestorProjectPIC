#!/bin/bash
echo "sincronizando estructura.."
python manage.py syncdb
echo "poblando base de datos .."
python manage.py loaddata datosIniciales2.json
echo "..Listo"
read -p "Presione enter para cerrar .."

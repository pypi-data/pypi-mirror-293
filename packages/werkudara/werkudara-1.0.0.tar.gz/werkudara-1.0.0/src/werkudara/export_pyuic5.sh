#!/bin/sh
# This script automatically converts each UI file (created using QtDesigner)
# under the folder ./ui into python files

# The base folder is relative to the repository's root folder.
base="./src/werkudara/ui"
base_exported="./src/werkudara/ui_exported"

# Export the UI files
ls $base | while read -r l; do
    exported_python_name=$(echo $l | sed -e 's/\.ui$/\.py/g')
    echo "Converting $l --> $exported_python_name"
    /bin/pyuic5 "$base/$l" -o "$base_exported/$exported_python_name"
done

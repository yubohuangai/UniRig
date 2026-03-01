#!/bin/bash
# Script to open Blender and import mesh files for viewing

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
PYTHON_SCRIPT="$SCRIPT_DIR/import_meshes_to_blender.py"

echo "Opening Blender with mesh files..."
echo "Script: $PYTHON_SCRIPT"
echo ""

# Launch Blender with the Python script (with GUI)
"$BLENDER" --python "$PYTHON_SCRIPT"

#!/bin/bash
# Script to open Blender and view PLY file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLENDER="/Applications/Blender.app/Contents/MacOS/Blender"
PYTHON_SCRIPT="$SCRIPT_DIR/view_ply.py"

echo "Opening Blender with PLY file..."
echo "File: /Users/yubo/github/FreeSplatter/output/gs_vis.ply"
echo ""

# Launch Blender with the Python script (with GUI)
"$BLENDER" --python "$PYTHON_SCRIPT"

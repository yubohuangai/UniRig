#!/usr/bin/env python3
"""
Blender script to import and view PLY files.
Run with: blender --python view_ply.py
"""

import bpy
from pathlib import Path

# PLY file to import
PLY_FILE = Path("/Users/yubo/github/FreeSplatter/output/gs_vis.ply")

def clear_scene():
    """Clear all objects from the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear orphaned data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)

def import_ply(filepath):
    """Import a PLY file."""
    try:
        bpy.ops.wm.ply_import(filepath=str(filepath))
        print(f"✓ Imported PLY: {filepath.name}")
        return True
    except Exception as e:
        print(f"✗ Error importing {filepath.name}: {e}")
        return False

def setup_viewport():
    """Setup viewport for better visualization."""
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'
                    space.shading.light = 'STUDIO'
                    space.shading.color_type = 'VERTEX'  # Show vertex colors
                    space.overlay.show_floor = True
                    space.overlay.show_axis_x = True
                    space.overlay.show_axis_y = True
                    space.overlay.show_axis_z = True

def main():
    """Main function to import and display PLY file."""
    print("\n" + "="*60)
    print("PLY Viewer - Importing PLY file into Blender")
    print("="*60 + "\n")
    
    if not PLY_FILE.exists():
        print(f"✗ File not found: {PLY_FILE}")
        return
    
    # Clear the scene
    print("Clearing scene...")
    clear_scene()
    
    # Import PLY file
    print(f"\nImporting: {PLY_FILE}")
    if import_ply(PLY_FILE):
        # Setup viewport
        print("\nSetting up viewport...")
        setup_viewport()
        
        # Frame the object in view
        try:
            bpy.ops.object.select_all(action='SELECT')
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    for region in area.regions:
                        if region.type == 'WINDOW':
                            with bpy.context.temp_override(area=area, region=region):
                                bpy.ops.view3d.view_all()
                            break
                    break
        except Exception as e:
            print(f"Note: Could not auto-frame view: {e}")
            print("Tip: Press 'Home' key in Blender to frame the object")
        
        print("\n" + "="*60)
        print("✓ Successfully imported PLY file")
        print("="*60 + "\n")
        
        print("Navigation Tips:")
        print("  - Pinch to zoom (trackpad)")
        print("  - Shift + Two-finger swipe to rotate")
        print("  - Two-finger swipe to pan")
        print("  - Press 'Z' for shading options")
        print("  - Press 'Home' to frame the object")
        print("\n💡 Point Cloud Display:")
        print("  - PLY files often contain point clouds")
        print("  - Try different shading modes with 'Z' key")
        print("  - Object Properties → Viewport Display to adjust point size")

if __name__ == "__main__":
    main()

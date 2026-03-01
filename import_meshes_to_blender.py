#!/usr/bin/env python3
"""
Blender script to import and view mesh files from UniRig results.
Run with: blender --python import_meshes_to_blender.py
"""

import bpy
import os
from pathlib import Path

# Define the results directory
RESULTS_DIR = Path("/Users/yubo/github/UniRig/results")

# List of mesh files to import
MESH_FILES = [
    # "mesh.glb",
    # "mesh_skeleton.fbx",
    # "mesh_skeleton_rigged.glb",
    # "mesh_skin.fbx",
    "mesh_skin_rigged.glb",
]

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
    for block in bpy.data.armatures:
        if block.users == 0:
            bpy.data.armatures.remove(block)

def import_file(filepath):
    """Import a file based on its extension."""
    ext = filepath.suffix.lower()
    
    try:
        if ext == '.fbx':
            bpy.ops.import_scene.fbx(filepath=str(filepath))
            print(f"✓ Imported FBX: {filepath.name}")
        elif ext == '.glb' or ext == '.gltf':
            bpy.ops.import_scene.gltf(filepath=str(filepath))
            print(f"✓ Imported GLB/GLTF: {filepath.name}")
        else:
            print(f"✗ Unsupported file format: {filepath.name}")
            return False
        return True
    except Exception as e:
        print(f"✗ Error importing {filepath.name}: {e}")
        return False

def arrange_objects_in_row(spacing=5.0):
    """Arrange all objects in a row for easy viewing."""
    objects = [obj for obj in bpy.data.objects if obj.type in ['MESH', 'ARMATURE', 'EMPTY']]
    
    for i, obj in enumerate(objects):
        obj.location.x = i * spacing
        obj.location.y = 0
        obj.location.z = 0

def setup_viewport():
    """Setup viewport for better visualization."""
    # Set to solid shading mode
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'SOLID'
                    space.shading.light = 'STUDIO'
                    space.shading.color_type = 'MATERIAL'
                    space.overlay.show_floor = True
                    space.overlay.show_axis_x = True
                    space.overlay.show_axis_y = True
                    space.overlay.show_axis_z = True
                    # Show bones as sticks instead of octahedral
                    space.overlay.show_relationship_lines = False

def setup_armature_display():
    """Configure armature (skeleton) display settings."""
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            # Set armature to display as stick/wire for cleaner view
            obj.data.display_type = 'STICK'
            # Show bones in front of mesh
            obj.show_in_front = True
            # Set bone colors
            for bone in obj.data.bones:
                bone.color.palette = 'THEME01'
    
    # Hide or delete icosphere mesh objects (these are bone joint visualizations from FBX import)
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and 'icosphere' in obj.name.lower():
            obj.hide_set(True)  # Hide them
            # Or delete them: bpy.data.objects.remove(obj, do_unlink=True)

def create_collection_for_each_file():
    """Create separate collections for each imported file."""
    collections = {}
    
    for i, filename in enumerate(MESH_FILES):
        filepath = RESULTS_DIR / filename
        if not filepath.exists():
            print(f"✗ File not found: {filepath}")
            continue
        
        # Create a new collection for this file
        collection_name = filepath.stem
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
        collections[filename] = collection
        
        # Remember currently existing objects
        existing_objects = set(bpy.data.objects)
        
        # Import the file
        if import_file(filepath):
            # Find newly imported objects
            new_objects = set(bpy.data.objects) - existing_objects
            
            # Separate mesh and armature objects
            mesh_objects = []
            armature_objects = []
            other_objects = []
            
            for obj in new_objects:
                # Unlink from all collections
                for coll in obj.users_collection:
                    coll.objects.unlink(obj)
                # Link to the new collection
                collection.objects.link(obj)
                
                # Categorize objects
                if obj.type == 'MESH':
                    mesh_objects.append(obj)
                elif obj.type == 'ARMATURE':
                    armature_objects.append(obj)
                else:
                    other_objects.append(obj)
            
            # Arrange objects: Files along Y-axis
            # Each file gets its own Y position
            y_offset = i * 3.0
            
            # Within each file, keep mesh and armature at the same location (overlapping)
            for obj in mesh_objects:
                obj.location.x = 0
                obj.location.y = y_offset
                obj.location.z = 0
            
            for obj in armature_objects:
                obj.location.x = 0
                obj.location.y = y_offset
                obj.location.z = 0
            
            for obj in other_objects:
                obj.location.x = 0
                obj.location.y = y_offset
                obj.location.z = 0
    
    return collections

def main():
    """Main function to import and display mesh files."""
    print("\n" + "="*60)
    print("UniRig Mesh Viewer - Importing mesh files into Blender")
    print("="*60 + "\n")
    
    # Clear the scene
    print("Clearing scene...")
    clear_scene()
    
    # Create collections and import files
    print("\nImporting files with separate collections:")
    collections = create_collection_for_each_file()
    
    # Setup viewport
    print("\nSetting up viewport...")
    setup_viewport()
    
    # Setup armature display (hide bone spheres, show as sticks)
    print("Configuring bone display...")
    setup_armature_display()
    
    # Frame all objects in view (do this last after everything is set up)
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
        print("Tip: Press 'Home' key in Blender to frame all objects")
    
    print("\n" + "="*60)
    print(f"✓ Successfully imported {len(collections)} file(s)")
    print("="*60 + "\n")
    
    print("Layout: Files arranged along Y-axis (top to bottom)")
    print("        Within each file: mesh (left) | armature (right)")
    print("Each file is in its own collection - you can toggle visibility in the Outliner.")
    print("\n🦴 Bone Display:")
    print("  - The icospheres have been hidden (they're bone joint markers from FBX)")
    print("  - Bones now display as sticks for cleaner visualization")
    print("  - To toggle bone visibility: Select armature → Object Data Properties → Viewport Display")
    print("\nTips:")
    print("  - Use mouse wheel to zoom")
    print("  - Shift + Two-finger swipe to rotate view (trackpad)")
    print("  - Two-finger swipe to pan (trackpad)")
    print("  - Press 'Z' for shading options")
    print("  - Press 'Home' key to frame all objects")
    print("  - Collections are visible in the Outliner (top-right)")
    print("\n💡 To see bone deformation:")
    print("  1. Select the armature (bone structure)")
    print("  2. Switch to Pose Mode (Ctrl+Tab or dropdown at top-left)")
    print("  3. Select and move bones to see how the mesh deforms")

if __name__ == "__main__":
    main()

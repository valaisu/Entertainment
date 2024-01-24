import bpy

def print(data):
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                bpy.ops.console.scrollback_append(override, text=str(data), type="OUTPUT")


print("starting...")

# Replace "Cube" with the name of your object
object_name = "chest"

# Replace "output.txt" with the desired file path and name
output_file_path = "output.txt"

# Get the object by name
obj = bpy.data.objects.get(object_name)

if obj and obj.type == 'MESH':
    mesh = obj.data

    with open(output_file_path, "w") as file:
        for face in mesh.polygons:
            face_coords = [mesh.vertices[i].co for i in face.vertices]
            face_coords_str = [f"{c[0]}, {c[1]}, {c[2]}" for c in face_coords]
            file.write(f"Face {face.index + 1} Coordinates: {', '.join(face_coords_str)}\n")

    print(f"Face vertex coordinates saved to {output_file_path}")
else:
    print(f"Object '{object_name}' not found or is not a mesh.")

print("done")

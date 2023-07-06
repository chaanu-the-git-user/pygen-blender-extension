import bpy
import bmesh

bl_info = {
    "name": "PyGen",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > PyGen",
    "description": "Generate Python code to recreate mesh objects",
    "category": "Development",
}

class PyGenOperator(bpy.types.Operator):
    bl_idname = "pygen.generate"
    bl_label = "Generate"
    
    def execute(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            
            code = "import bpy\n\n"
            code += "context = bpy.context\n"
            code += f"obj = context.active_object\n\n"
            
            code += f"mesh_data = bpy.data.meshes.new('{obj.name}')\n"
            
            code += "vertices = [\n"
            for vert in bm.verts:
                code += f"\t({vert.co.x}, {vert.co.y}, {vert.co.z}),\n"
            code += "]\n\n"
            
            code += "edges = [\n"
            for edge in bm.edges:
                code += f"\t({edge.verts[0].index}, {edge.verts[1].index}),\n"
            code += "]\n\n"
            
            code += "faces = [\n"
            for face in bm.faces:
                code += "\t["
                for vert in face.verts:
                    code += f"{vert.index}, "
                code = code[:-2]  # Remove the last comma and space
                code += "],\n"
            code += "]\n\n"
            
            code += "mesh_data.from_pydata(vertices, edges, faces)\n"
            code += "mesh_data.update()\n\n"
            
            code += f"obj = bpy.data.objects.new('{obj.name}', mesh_data)\n"
            code += "context.collection.objects.link(obj)\n"
            
            text_block = bpy.data.texts.new("Generated Code")
            text_block.from_string(code)
            
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, "No active mesh object found")
            return {'CANCELLED'}

class PyGenPanel(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_pygen"
    bl_label = "PyGen"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "PyGen"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("pygen.generate", text="Generate")

classes = (PyGenOperator, PyGenPanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

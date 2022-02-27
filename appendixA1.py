import bpy

# user sepcified object name
object_name = 'Cube'

o = bpy.data.objects[object_name]
normals = [p.normal for p in o.data.polygons]

import numpy as np
resultant_normal = np.add.reduce(normals)

magnitude = np.linalg.norm(resultant_normal)
unit_vector = resultant_normal / magnitude
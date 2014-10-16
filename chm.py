import struct
import sys
import tag
import mesh

class Chm:
    tagtree = None
    info = None
    quan = None
    material_set = None
    animation_set = None
    mesh_set = None
    node_set = None
    bank = None
    def __init__(self, root_tag):
        if root_tag.type != b"CHM ":
            raise Exception("File is not a valid CHM file!")
        self.tagtree = root_tag
        self.material_set = []
        self.animation_set = []
        self.mesh_set = []
        self.node_set = []
        for subtag in self.tagtree.subtags:
            if subtag.type == b"MSST": # Mesh set
                for mesh_tag in subtag.subtags:
                    self.mesh_set.append(mesh.Mesh(mesh_tag))
    def chm2obj(self):
        objs = []
        for mesh in self.mesh_set:
            objs.append(mesh.mesh2obj())
        return objs
        
# If called as script, write obj file for each mesh
if __name__ == "__main__":
    fh = open(sys.argv[1], "rb")
    tagroot = tag.Tag(fh)
    chm = Chm(tagroot)
    objs = chm.chm2obj()
    for obj in objs:
        fo = open("%s_%s.obj" % (sys.argv[1], obj["name"]), "w")
        fo.write(obj["vertices"])
        fo.write(obj["normals"])
        fo.write(obj["uv"])
        fo.write(obj["faces"])
        fo.close()
    fh.close()
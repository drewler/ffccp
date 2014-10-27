import sys
import tag
import mesh
import node
import os

class Chm:
    tagtree = None
    info = None
    quan = None
    material_set = None
    animation_set = None
    mesh_set = None
    node_set = None
    skeleton = None
    bank = None
    def __init__(self, root_tag):
        if root_tag.type != b"CHM ":
            raise Exception("File is not a valid CHM file!")
        self.tagtree = root_tag
        self.material_set = []
        self.animation_set = []
        self.mesh_set = []
        self.node_set = []
        self.skeleton = {}
        for subtag in self.tagtree.subtags:
            if subtag.type == b"MSST": # Mesh set
                for mesh_tag in subtag.subtags:
                    self.mesh_set.append(mesh.Mesh(mesh_tag))
            if subtag.type == b"NSET": # Node set
                for node_tag in subtag.subtags:
                    new_node = node.Node(node_tag)
                    tmp_id = new_node.info[2:4]
                    tmp_magic = new_node.info[10:12]
                    if tmp_magic == self.cur_magic:
                        
            
        self.cur_magic = tmp_magic
        self.cur_id = tmp_id
        
                    #self.node_set.append(node.Node(node_tag))
    def chm2obj(self):
        objs = []
        for mesh in self.mesh_set:
            objs.append(mesh.mesh2obj())
        #for node in self.node_set:
        #    node.tfrm2obj()
        #for node in self.node_set:
        #    node.inf2obj()
        #for node in self.node_set:
        #    node.binf2obj()
        return objs
        
# If called as script, write obj file for each mesh
if __name__ == "__main__":
    fh = open(sys.argv[1], "rb")
    if (len(sys.argv[1]) > 4 and sys.argv[1][-3:] == "chm") and not os.path.exists(sys.argv[1][:-4]):
        os.makedirs(sys.argv[1][:-4])
    tagroot = tag.Tag(fh)
    chm = Chm(tagroot)
    objs = chm.chm2obj()
    for obj in objs:
        fo = open("%s/%s.obj" % (sys.argv[1][:-4], obj["name"]), "w")
        fo.write(obj["vertices"])
        fo.write(obj["normals"])
        fo.write(obj["uv"])
        fo.write(obj["faces"])
        fo.close()
    fh.close()
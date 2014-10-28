import sys
import tag
import mesh
import node
import os
import struct

class Chm:
    tagtree = None
    info = None
    quan = None
    material_set = None
    animation_set = None
    mesh_set = None
    node_set = None
    skeleton = None
    cur_node = None
    bank = None
    def __init__(self, root_tag):
        if root_tag.type != b"CHM ":
            raise Exception("File is not a valid CHM file!")
        self.tagtree = root_tag
        self.material_set = []
        self.animation_set = []
        self.mesh_set = []
        self.node_set = []
        self.skeleton = { "parent" : None, "id" : 0, "node" : None, "children" : [] }
        self.cur_node = self.skeleton
        skelstart = False
        for subtag in self.tagtree.subtags:
            if subtag.type == b"MSST": # Mesh set
                for mesh_tag in subtag.subtags:
                    self.mesh_set.append(mesh.Mesh(mesh_tag))
            if subtag.type == b"NSET": # Node set
                for node_tag in subtag.subtags:
                    new_node = node.Node(node_tag)
                    tmp_id = struct.unpack(">H", new_node.info[2:4])[0]
                    tmp_magic = new_node.info[10:12]
                    if not skelstart:
                        
                        if tmp_id == 1:
                            self.cur_node["node"] = new_node
                            self.cur_node["id"] = tmp_id
                            skelstart = True
                    else:
                        
                        if tmp_magic == self.cur_node["node"].info[10:12]:
                            # Find node
                            n = self.find_node(self.skeleton["children"], tmp_id)
                            if n != None:
                                self.cur_node = n
                        else:
                            c = { "parent" : self.cur_node, "id" : tmp_id, "node" : new_node, "children" : [] }
                            self.cur_node["children"].append(c)
                            self.cur_node = c   
                        
                    self.node_set.append(node.Node(node_tag))
        self.print_skeleton()
    def print_skeleton(self):
        self.print_node(self.skeleton)
    def print_node(self, e, depth = 0):
        print "%s>%s" % ("-" * depth, e["node"].name)
        if e["children"] != []:
            for c in e["children"]:
                self.print_node(c, depth+1)
    def find_node(self, level, id):
        for e in level:
            if e["id"] == id:
                return e
            else:
                t = self.find_node(e["children"], id)
                if t != None:
                    return t
        return None
        
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
import sys
import tag
import mesh
import node
import os
import struct
import math

def normalize(v):
    vmag = math.sqrt(v[0]**v[0] + v[1]**v[1] + v[2]**v[2])
    return [ v[i]/vmag  for i in range(len(v)) ]

def q_to_axisangle(q):
    w, v = q[3], q[:3]
    theta = math.acos(w) * 2.0
    return normalize(v), theta

class Chm:
    tagtree = None
    info = None
    scale = None
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
        self.skeleton = { "parent" : None, "id" : None, "node" : None, "children" : [] }
        for subtag in self.tagtree.subtags:
            if subtag.type == b"INFO":
                self.parse_info(subtag)
            elif subtag.type == b"QUAN":
                self.parse_quan(subtag)
            elif subtag.type == b"MSST": # Mesh set
                for mesh_tag in subtag.subtags:
                    self.mesh_set.append(mesh.Mesh(mesh_tag))
            elif subtag.type == b"NSET": # Node set
                self.parse_nodeset(subtag)
    def parse_info(self, info_tag):
        self.info = struct.unpack(">%if" % (info_tag.length/4.0), info_tag.binary_data)
        print("info: %s" % str(self.info))
        info2 = []
        info3 = []
        for e in self.info:
            info2.append(math.degrees(e))
            info3.append(90*e)
        print(info2)
        print(info3)
        print("quat: %s" % str(q_to_axisangle((self.info[0],self.info[1],self.info[2],self.info[3]))))
    def parse_quan(self, quan_tag):
        self.scale = 1.0/(2.0**struct.unpack(">I",quan_tag.binary_data[0:4])[0])
        print("quan: %s" % str(struct.unpack(">%ii" % (quan_tag.length/4.0), quan_tag.binary_data)))
    def parse_nodeset(self, subtag):
        skelstart = False
        cur_id = 0
        cur_node = self.skeleton
        for node_tag in subtag.subtags:
            new_node = node.Node(node_tag)
            tmp_id = struct.unpack(">H", new_node.info[2:4])[0]
            tmp_magic = new_node.info[10:12]
            if not skelstart:
                if tmp_id == 0:
                    cur_node["node"] = new_node
                    cur_node["id"] = tmp_id
                    skelstart = True
                    cur_id += 1
            else:
                if tmp_magic == cur_node["node"].info[10:12]:
                    n = self.find_node(self.skeleton["children"], tmp_id - 1)
                    if n != None:
                        cur_node = n
                
                c = { "parent" : cur_node, "id" : cur_id, "node" : new_node, "children" : [] }
                cur_node["children"].append(c)
                cur_node = c   
                cur_id += 1
            self.node_set.append(node.Node(node_tag))
    def print_skel(self, e, depth = 0):
        print("%s %s (id: %s)" % ("x" * depth, e["node"].name, hex(e["id"])))
        if e["children"] != []:
            for c in e["children"]:
                self.print_skel(c, depth + 1)
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
        # self.print_skel(self.skeleton)
        for mesh in self.mesh_set:
            objs.append(mesh.mesh2obj())
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
        fo = open("%s/%s.obj" % (sys.argv[1][:-4], obj["name"]), "w+")
        fo.write(obj["vertices"])
        fo.write(obj["normals"])
        fo.write(obj["uv"])
        fo.write(obj["faces"])
        fo.close()
    fh.close()
    sys.exit(0)

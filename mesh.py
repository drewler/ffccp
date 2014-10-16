import struct
import sys
import tag
import dlhd

class Mesh:
    name = None
    vertices = None
    normals = None
    texcoor = None
    skin = None
    dlhd = None
    def __init__(self, mesh_tag):
        if mesh_tag.type != b"MESH":
            raise Exception("Tag is not a valid MESH tag!")
        self.vertices = []
        self.normals = []
        self.texcoor = []
        for mesh_subtag in mesh_tag.subtags:
            if mesh_subtag.type == b"MNAM":
                self.parse_name(mesh_subtag)
            elif mesh_subtag.type == b"VERT":
                self.parse_vertices(mesh_subtag)
            elif mesh_subtag.type == b"NORM":
                self.parse_normals(mesh_subtag)
            elif mesh_subtag.type == b"UV  ":
                self.parse_uv(mesh_subtag)
            elif mesh_subtag.type == b"SKIN":
                self.parse_skin(mesh_subtag)
            elif mesh_subtag.type == b"DLHD":
                self.parse_dlhd(mesh_subtag)
            else:
                print "Unrecognized MESH subtag : %s" % mesh_subtag.type
    def parse_name(self, name_tag):
        self.name = name_tag.binary_data[0:name_tag.length-1]
    def parse_vertices(self, vert_tag):
        bytes_read = 0
        while bytes_read < vert_tag.length:
            vertex = struct.unpack(">hhh", vert_tag.binary_data[bytes_read:bytes_read+6])
            self.vertices.append((vertex[0]/100.0, vertex[1]/100.0, vertex[2]/100.0))
            bytes_read += 6
    def parse_normals(self, norm_tag):
        bytes_read = 0
        while bytes_read < norm_tag.length:
            normal = struct.unpack('>hhh', norm_tag.binary_data[bytes_read:bytes_read+6])
            self.normals.append((normal[0]/100.0, normal[1]/100.0, normal[2]/100.0))
            bytes_read += 6
    def parse_uv(self, uv_tag):
        bytes_read = 0
        while bytes_read < uv_tag.length:
            uv = struct.unpack('>hh', uv_tag.binary_data[bytes_read:bytes_read+4])
            self.texcoor.append((uv[0]/4096.0, uv[1]/4096.0))
            bytes_read += 4
    def parse_skin(self, skin_tag):
        return 0 # TO-DO
    def parse_dlhd(self, dlhd_tag):
        self.dlhd = dlhd.Dlhd(dlhd_tag)
    def vertices2obj(self):
        vobj = ""
        for vertex in self.vertices:
            vobj = "".join([vobj, "v %f %f %f\n" % vertex])
        return vobj
    def normals2obj(self):
        nobj = ""
        for normal in self.normals:
            nobj = "".join([nobj, "vn %f %f %f\n" % normal])
        return nobj
    def texcoor2obj(self):
        tobj = ""
        for uv in self.texcoor:
            tobj = "".join([tobj, "vt %f %f\n" % uv])
        return tobj
    def mesh2obj(self):
        if self.vertices == [] or self.normals == [] or self.texcoor == []:
            print "MESH data is missing sections"
            return None
        obj = {}
        obj["name"] = self.name
        obj["vertices"] = self.vertices2obj()
        obj["normals"] = self.normals2obj()
        obj["uv"] = self.texcoor2obj()
        obj["faces"] = self.dlhd.dlhd2obj(self)
        return obj
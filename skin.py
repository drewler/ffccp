import struct
import sys
import tag
import collections

class Skin:
    nodelst = None
    one = None
    max1 = None
    max2 = None
    normals = None
    def __init__(self, skin_tag):
        self.nodelst = []
        self.one = []
        self.normals = {}
        self.max1 = self.max2 = 0
        for skin_subtag in skin_tag.subtags:
            if skin_subtag.type == b"NODE":
                self.parse_node(skin_subtag)
            elif skin_subtag.type == b"ONE ":
               self.parse_one(skin_subtag)
            else:
                print("Unrecognized SKIN subtag : %s" % skin_subtag.type)
        # print(self.normals)
        # print("m1: %s - m2: %s" % (self.max1, self.max2))
        # for e in self.one:
            # print("> %s - nel: %i" % (e["gid"], e["nel"]))
            # print("\t%s" % str(e["elems"]))
            # for w in e["elems"]:
                # print("\t%s" % hex(w))
        # for i, n in enumerate(self.nodelst):
            # print("node %i - bone: %s, vertices: %s" % (i, hex(n["bone"]), n["vertices"]))
    def parse_node(self, node_tag):
        bone = struct.unpack('>I', node_tag.binary_data[0:node_tag.length])[0]
        new_sknode = { "bone" : bone, "vertices" : [] }
        self.nodelst.append(new_sknode)
    def parse_one(self, one_tag):
        bytes_read = 0
        # xx => skin node index
        # xx => vertex index
        # xx => number of following elements
        # xx * nel => elements (vertex normals)
        while bytes_read < one_tag.length:
            gid = struct.unpack('>2H', one_tag.binary_data[bytes_read:bytes_read+4])
            bytes_read += 4
            nel = struct.unpack('>H', one_tag.binary_data[bytes_read:bytes_read+2])[0]
            bytes_read += 2
            elems = struct.unpack('>%iH' % nel, one_tag.binary_data[bytes_read:bytes_read+nel*2])
            bytes_read += nel*2
            self.nodelst[gid[0]]["vertices"].append(gid[1])
            # print(gid[1])
            self.normals[gid[1]] = list(elems)
            #self.one.append({"gid" : gid, "nel" : nel, "elems" : elems})
            # if gid[0] > self.max1:
                # self.max1 = gid[0]
            # for e in elems:
                # if e > self.max2:
                    # self.max2 = e
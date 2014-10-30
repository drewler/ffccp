import struct
import sys
import tag
import collections

class Skin:
    nodelst = None
    one = None
    max1 = None
    max2 = None
    def __init__(self, skin_tag):
        self.nodelst = []
        self.one = []
        self.max1 = self.max2 = 0
        for skin_subtag in skin_tag.subtags:
            if skin_subtag.type == b"NODE":
                self.parse_node(skin_subtag)
            elif skin_subtag.type == b"ONE ":
               self.parse_one(skin_subtag)
            else:
                print("Unrecognized SKIN subtag : %s" % skin_subtag.type)
        print("m1: %s - m2: %s" % (self.max1, self.max2))
        for e in self.one:
            print("> %s - nel: %i" % (e["gid"], e["nel"]))
            print("\t%s" % str(e["elems"]))
            # for w in e["elems"]:
                # print("\t%s" % hex(w))
    def parse_node(self, node_tag):
        self.nodelst.append(struct.unpack('>2H', node_tag.binary_data[0:node_tag.length]))
    def parse_one(self, one_tag):
        print(one_tag.length)
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
            self.one.append({"gid" : gid, "nel" : nel, "elems" : elems})
            # if gid[0] > self.max1:
                # self.max1 = gid[0]
            # for e in elems:
                # if e > self.max2:
                    # self.max2 = e
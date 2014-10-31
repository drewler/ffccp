import struct
import sys
import tag
import os

class Cha:
    frames = None
    nodes = None
    max = None
    def __init__(self, root_tag):
        if root_tag.type != b"CHA ":
            raise Exception("File is not a valid CHA file!")
        self.nodes = []
        self.max = 0
        for subtag in root_tag.subtags:
            if subtag.type == b"ANIM": # Anim set
                for aset_tag in subtag.subtags:
                    if aset_tag.type == b"FRAM":
                        self.parse_anim_frames(aset_tag)
                    elif aset_tag.type == b"INFO":
                        self.parse_anim_info(aset_tag)
                    elif aset_tag.type == b"NODE":
                        new_node = {}
                        for sn_tag in aset_tag.subtags:
                            if sn_tag.type == b"NAME":
                                self.parse_node_name(sn_tag, new_node)
                            elif sn_tag.type == b"DATA":
                                self.parse_node_data(sn_tag, new_node)
                        self.nodes.append(new_node)
                    elif aset_tag.type == b"BANK":
                        self.parse_anim_bank(aset_tag)
        print("max: %i (%s)" % (self.max, hex(self.max)))
    def parse_anim_frames(self, frame_tag):
        self.frames = struct.unpack(">i", frame_tag.binary_data)
    def parse_anim_info(self, info_tag):
        self.info = struct.unpack(">%ii" % (info_tag.length/4), info_tag.binary_data)
        print self.info
    def parse_node_name(self, name_tag, node):
        node["name"] = name_tag.binary_data[0:name_tag.length-1].decode("ascii")
    def parse_node_data(self, node_tag, node):
        node["data"] = struct.unpack(">%iI" % (node_tag.length/4), node_tag.binary_data)
        for e in node["data"]:
            if e > self.max:
                self.max = e
    def parse_anim_bank(self, bank_tag):
        return 0 # TO-DO
        
        
# If called as script, write img file for each texture
if __name__ == "__main__":
    fh = open(sys.argv[1], "rb")
    #if (len(sys.argv[1]) > 4 and sys.argv[1][-3:] == "cha") and not os.path.exists(sys.argv[1][:-4]):
    #    os.makedirs(sys.argv[1][:-4])
    tagroot = tag.Tag(fh)
    cha = Cha(tagroot)
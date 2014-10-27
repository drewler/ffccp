import struct
import re

class Node:
    info = None
    name = None
    name2 = None
    tfrm = None
    binf = None
    mesh_index = None
    def __init__(self, node_tag):
        if node_tag.type != b"NODE":
            raise Exception("Tag is not a valid NODE tag!")
        for node_subtag in node_tag.subtags:
            if node_subtag.type == b"INFO":
                self.parse_info(node_subtag)
            elif node_subtag.type == b"NAME":
                self.parse_name(node_subtag)
            elif node_subtag.type == b"NAM2":
                self.parse_name2(node_subtag)
            elif node_subtag.type == b"TFRM":
                self.parse_tfrm(node_subtag)
            elif node_subtag.type == b"BINF":
                self.parse_binf(node_subtag)
            elif node_subtag.type == b"MIDX":
                self.parse_midx(node_subtag)
            else:
                print "Unrecognized NODE subtag : %s" % node_subtag.type
    def parse_info(self, info_tag):
        self.info = info_tag.binary_data
    def parse_name(self, name_tag):
        self.name = name_tag.binary_data[0:name_tag.length-1]
    def parse_name2(self, name_tag):
        self.name2 = name_tag.binary_data[0:name_tag.length-1]
    def parse_tfrm(self, tfrm_tag):
        #self.tfrm = struct.unpack(">" + "hh"*12, tfrm_tag.binary_data[0:tfrm_tag.length]) # shorts
        #self.tfrm = [i/100.0 for i in struct.unpack(">" + "hh"*12, tfrm_tag.binary_data[0:tfrm_tag.length])] # shorts scaled
        #self.tfrm = struct.unpack(">" + "ff"*6, tfrm_tag.binary_data[0:tfrm_tag.length])  # floats
        #self.tfrm = struct.unpack(">" + "ii"*6, tfrm_tag.binary_data[0:tfrm_tag.length])  # integers
        #self.tfrm = struct.unpack(">" + "dd"*3, tfrm_tag.binary_data[0:tfrm_tag.length])  # doubles
        bytes_read = 0
        self.tfrm = []
        while bytes_read < tfrm_tag.length:
            self.tfrm.append(struct.unpack(">4f", tfrm_tag.binary_data[bytes_read:bytes_read+16]))  # floats
            bytes_read += 16
            #self.tfrm.append(struct.unpack(">" + "ffff", tfrm_tag.binary_data[bytes_read:bytes_read+16]))  # floats
            #bytes_read += 16
            #self.tfrm.append(struct.unpack(">" + "fff", tfrm_tag.binary_data[bytes_read:bytes_read+12]))  # floats
            #bytes_read += 12
            #self.tfrm.append([i/100.0 for i in struct.unpack(">" + "hhh", tfrm_tag.binary_data[bytes_read:bytes_read+6])])  # floats
            #bytes_read += 6
    def parse_binf(self, binf_tag):
        #self.binf = struct.unpack(">" + "hh"*4, binf_tag.binary_data[0:binf_tag.length])  # shorts
        #self.binf = [i/100.0 for i in struct.unpack(">" + "hh"*4, binf_tag.binary_data[0:binf_tag.length])]  # shorts scaled
        self.binf = binf_tag.binary_data # struct.unpack(">" + "ff"*2, binf_tag.binary_data[0:binf_tag.length])  # floats
        #self.binf = struct.unpack(">" + "ii"*2, binf_tag.binary_data[0:binf_tag.length])  # integers
        #self.binf = struct.unpack(">" + "dd"*1, binf_tag.binary_data[0:binf_tag.length])  # doubles
    def parse_midx(self, midx_tag):
        self.mesh_index = struct.unpack(">L", midx_tag.binary_data[0:4])
    def tfrm2obj(self):
        print "\t tfrm : "
        for t in self.tfrm:
            print "\t\t %s" % str(t)
        print "\t\t %s" % str((0.0, 0.0, 0.0, 1.0))
    def inf2obj(self):
        if self.info != None:
            tmp = re.findall("..", self.info.encode('hex'))
            res = []
            for e in tmp:
                res.append(bin(int(e,16))[2:].zfill(8))
            res = tmp
            print "node info : %s - %s, %s" % (res, self.name, self.name2)
    def binf2obj(self):
        if self.binf != None:
            tmp = re.findall("..", self.binf.encode('hex'))
            res = []
            for e in tmp:
                res.append(bin(int(e,16))[2:].zfill(8))
            res = tmp
            print "node binf : %s - %s, %s" % (res, self.name, self.name2)
    def midx2obj(self):
        if self.mesh_index != None:
            print "node midx : %s - %s, %s" % (str(self.mesh_index), self.name, self.name2)
        
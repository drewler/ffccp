import struct
import re
import numpy as np

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
        #print "%s, %s" % (self.info[2:4].encode('hex'), self.info[10:12].encode('hex'))
    def parse_name(self, name_tag):
        self.name = name_tag.binary_data[0:name_tag.length-1]
    def parse_name2(self, name_tag):
        self.name2 = name_tag.binary_data[0:name_tag.length-1]
    def parse_tfrm(self, tfrm_tag):
        bytes_read = 0
        self.tfrm = np.zeros((4,4))
        while bytes_read < tfrm_tag.length:
            self.tfrm[bytes_read/16,:] = struct.unpack(">4f", tfrm_tag.binary_data[bytes_read:bytes_read+16])  # floats
            bytes_read += 16
        self.tfrm[3,3] = 1.0;
    def parse_binf(self, binf_tag):
        #self.binf = struct.unpack(">16B", binf_tag.binary_data[0:binf_tag.length])  # byte
        #self.binf = struct.unpack(">8h", binf_tag.binary_data[0:binf_tag.length])  # shorts
        #self.binf = [i/100.0 for i in struct.unpack(">" + "hh"*4, binf_tag.binary_data[0:binf_tag.length])]  # shorts scaled
        #self.binf = binf_tag.binary_data 
        self.binf = []
        self.binf.append(struct.unpack(">2h", binf_tag.binary_data[0:4]))
        self.binf.append(struct.unpack(">3f", binf_tag.binary_data[4:16]))  # floats
        #self.binf.append(struct.unpack(">4f", binf_tag.binary_data[0:16])) 
        #self.binf = struct.unpack(">" + "ii"*2, binf_tag.binary_data[0:binf_tag.length])  # integers
        #self.binf = struct.unpack(">" + "dd"*1, binf_tag.binary_data[0:binf_tag.length])  # doubles
    def parse_midx(self, midx_tag):
        self.mesh_index = struct.unpack(">L", midx_tag.binary_data[0:4])
    def tfrm2obj(self):
        print "node tfrm - %s, %s : " % (self.name, self.name2)
        x = self.tfrm[0:3,0]
        tail = self.tfrm[0:3,1]
        z = self.tfrm[0:3,2]
        head = self.tfrm[0:3,3]
        r = np.cross(tail, z)
        print "x    = %s" % x
        print "tail = %s" % tail
        print "z    = %s" % z
        print "head = %s" % head
        #print np.cross(tail, z)
        #print "is x = cross(tail, z)? : %s" % np.array_equal(np.around(x,4),np.around(np.cross(tail, z),4))
    def mat3_to_vec_roll(self, mat):
        tail = mat.col[1]
        tailmat = vec_roll_to_mat3(tail, 0)
        tailmatinv = tailmat.inverted()
        rollmat = tailmatinv * mat
        roll = math.atan2(rollmat[0][2], rollmat[2][2])
        return tail, roll
    def inf2obj(self):
        if self.info != None:
            tmp = re.findall("....", self.info.encode('hex'))
            res = []
            for e in tmp:
                res.append(bin(int(e,16))[2:].zfill(8))
            res = tmp
            print "node info : %s - %s, %s" % (res, self.name, self.name2)
    def binf2obj(self):
        if self.binf != None:
            #tmp = re.findall("....", self.binf.encode('hex'))
            #res = []
            #for e in tmp:
            #    res.append(bin(int(e,16))[2:].zfill(8))
            #res = tmp
            res = self.binf
            print "node binf : %s - %s, %s" % (res, self.name, self.name2)
    def midx2obj(self):
        if self.mesh_index != None:
            print "node midx : %s - %s, %s" % (str(self.mesh_index), self.name, self.name2)
        
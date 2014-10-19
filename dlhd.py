import struct
import sys
import tag

class Dlhd:
    dlsts = None
    def __init__(self, dlhd_tag):
        self.dlsts = []
        for dlhd_subtag in dlhd_tag.subtags:
            if dlhd_subtag.type == b"DLST":
                self.parse_dlst(dlhd_subtag)
            else:
                print "Unrecognized DLHD subtag : %s" % dlhd_subtag.type
    def parse_dlst(self, dlst_tag):
        bytes_read = 0
        lst = []
        while bytes_read < dlst_tag.length:
            dlst = { "ltype" : 0, "size" : 0, "data" : [] }
            dlst["ltype"] = struct.unpack('>B', dlst_tag.binary_data[bytes_read:bytes_read+1])[0]
            bytes_read += 1
            if dlst["ltype"] < 0x90:
                continue
            dlst["size"] = struct.unpack('>H', dlst_tag.binary_data[bytes_read:bytes_read+2])[0]
            bytes_read += 2
            dlst_count = 0
            if (hex(dlst["ltype"]) in ('0x98', '0x99')) or (hex(dlst["ltype"]) in ('0x90', '0x91')):
                while dlst_count < dlst["size"]:
                    dlst["data"].append(struct.unpack('>HHHH', dlst_tag.binary_data[bytes_read:bytes_read+8]))
                    bytes_read += 8
                    dlst_count += 1
            elif (hex(dlst["ltype"]) in ('0x92', '0x9a')):
                while dlst_count < dlst["size"]:
                    dlst["data"].append(struct.unpack('>HHHHH', dlst_tag.binary_data[bytes_read:bytes_read+10]))
                    bytes_read += 10
                    dlst_count += 1
            else:
                raise Exception("Unknown DLST type: %s\n" % hex(dlst["ltype"]))
            lst.append(dlst)
        self.dlsts.append(lst)
    def dlst2obj(self, dlst):
        fobj = ""
        for lst in dlst:
            if (hex(lst["ltype"]) in ('0x98', '0x99')):
                for i in range(1, len(lst["data"])-1):
                    fc0 = "%i/%i/%i" % (lst["data"][i-(i%2)][0]+1, lst["data"][i-(i%2)][3]+1, lst["data"][i-(i%2)][1]+1)
                    fc1 = "%i/%i/%i" % (lst["data"][i-((i+1)%2)][0]+1, lst["data"][i-((i+1)%2)][3]+1, lst["data"][i-((i+1)%2)][1]+1)
                    fc2 = "%i/%i/%i" % (lst["data"][i+1][0]+1, lst["data"][i+1][3]+1, lst["data"][i+1][1]+1)
                    fobj = "".join([fobj, "f %s %s %s\n" % (fc0, fc1, fc2)])
            elif (hex(lst["ltype"]) in ('0x90', '0x91')):
                for i in range(0, len(lst["data"])-2, 3):
                    fc0 = "%i/%i/%i" % (lst["data"][i][0]+1, lst["data"][i][3]+1, lst["data"][i][1]+1)
                    fc1 = "%i/%i/%i" % (lst["data"][i+1][0]+1, lst["data"][i+1][3]+1, lst["data"][i+1][1]+1)
                    fc2 = "%i/%i/%i" % (lst["data"][i+2][0]+1, lst["data"][i+2][3]+1, lst["data"][i+2][1]+1)
                    fobj = "".join([fobj, "f %s %s %s\n" % (fc0, fc1, fc2)])
            elif (hex(lst["ltype"]) in ('0x92', '0x9a')):
                for i in range(1, len(lst["data"])-1):
                    fc0 = "%i/%i/%i" % (lst["data"][i-(i%2)][0]+1, lst["data"][i-(i%2)][3]+1, lst["data"][i-(i%2)][1]+1)
                    fc1 = "%i/%i/%i" % (lst["data"][i-((i+1)%2)][0]+1, lst["data"][i-((i+1)%2)][3]+1, lst["data"][i-((i+1)%2)][1]+1)
                    fc2 = "%i/%i/%i" % (lst["data"][i+1][0]+1, lst["data"][i+1][3]+1, lst["data"][i+1][1]+1)
                    fobj = "".join([fobj, "f %s %s %s\n" % (fc0, fc1, fc2)])
            else:
                raise Exception("Unknown lst type: %s\n" % hex(lst["ltype"]))
        return fobj
    def dlhd2obj(self, mesh):
        if self.dlsts == []:
            print "DLHD data is missing sections"
            return None
        dobj = ""
        gcount = 0
        for dlst in self.dlsts:
            dobj = "".join([dobj, "g %s.%i\n" % (mesh.name, gcount), self.dlst2obj(dlst)])
            gcount += 1
        return dobj
import struct

class Matl:
    tidx = None
    name = None
    atrb = None
    bump = None
    def __init__(self, matl_tag):
        if matl_tag.type != b"MATL":
            raise Exception("Tag is not a valid MATL tag!")
        for matl_subtag in matl_tag.subtags:
            if matl_subtag.type == b"NAME":
                self.parse_name(matl_subtag)
            elif matl_subtag.type == b"TIDX":
                self.parse_tidx(matl_subtag)
            elif matl_subtag.type == b"ATRB":
                self.parse_atrb(matl_subtag)
            # elif matl_subtag.type == b"BUMP":
                # continue
            else:
                print("Unrecognized MATL subtag : %s" % matl_subtag.type)
        print("MATL NAME: %s" % self.name)
        print("MATL TIDX: %s" % str(self.tidx))
    def parse_name(self, name_tag):
        self.name = name_tag.binary_data[0:name_tag.length-1].decode("ascii")
    def parse_tidx(self, tidx_tag):
        ntex = struct.unpack(">I", tidx_tag.mystery_data[0:4])
        self.tidx = struct.unpack(">%iI" % ntex, tidx_tag.binary_data[0:tidx_tag.length])
    def parse_atrb(self, atrb_tag):
        natrb = struct.unpack(">I", atrb_tag.mystery_data[0:4])
        # for i in range(0, natrb):
            # self.atrb.append(struct.unpack())
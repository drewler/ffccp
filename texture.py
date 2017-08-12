import struct
import sys
import numpy as np

class Texture:
    name = None
    fmt = None
    size = None
    image = None
    def __init__(self, texture_tag):
        if texture_tag.type != b"TXTR":
            raise Exception("Tag is not a valid TXTR tag!")
        for texture_subtag in texture_tag.subtags:
            if texture_subtag.type == b"NAME":
                self.parse_name(texture_subtag)
            elif texture_subtag.type == b"FMT ":
                self.parse_fmt(texture_subtag)
            elif texture_subtag.type == b"SIZE":
                self.parse_size(texture_subtag)
            elif texture_subtag.type == b"IMAG":
                self.parse_image(texture_subtag)
            else:
                print("Unrecognized TXTR subtag : %s" % texture_subtag.type)
    def parse_name(self, name_tag):
        self.name = name_tag.binary_data[0:name_tag.length-1].decode("ascii")
    def parse_fmt(self, fmt_tag):
        self.fmt = fmt_tag.binary_data[0:3]
    def parse_size(self, size_tag):
        self.size = struct.unpack(">LL", size_tag.binary_data[0:8])
    def parse_image(self, image_tag):
        if self.fmt == b"\x06\x01\x01": # CMPR
            self.image = np.zeros((self.size[1],self.size[0],4), dtype=np.uint8)
            self.cmpr(image_tag)
        else:
            print("Unrecognized texture fmt: %s" % self.fmt)
    def cmpr_subtile(self, subtile_data, x_offset, y_offset, cur_x, cur_y):
        COLOR0, COLOR1 = struct.unpack(">HH", subtile_data[0:4])
        RGB = [None, None, None, None]
        A   = [None, None, None, None]
        RGB[0] = bin(COLOR0)[2:].zfill(16)
        RGB[0] = np.array([255/31 * int(RGB[0][0:5],2), 255/63 * int(RGB[0][5:11],2), 255/31 * int(RGB[0][11:16],2)])
        A[0] = 255
        RGB[1] = bin(COLOR1)[2:].zfill(16)
        RGB[1] = np.array([255/31 * int(RGB[1][0:5],2), 255/63 * int(RGB[1][5:11],2), 255/31 * int(RGB[1][11:16],2)])
        A[1] = 255
        if COLOR0 > COLOR1:
            RGB[2] = (2 * RGB[0] + RGB[1])/3
            A[2] = 255
            RGB[3] = (2 * RGB[1] + RGB[0])/3
            A[3] = 255
        else:
            RGB[2] = (RGB[0] + RGB[1])/2
            A[2] = 255
            RGB[3] = (2 * RGB[1] + RGB[0])/3
            A[3] = 0
        texel_idx = struct.unpack(">I", subtile_data[4:8])
        texel_idx = bin(texel_idx[0])[2:].zfill(32)
        for y in range(0,4):
            for x in range(0,4):
                idx = int(texel_idx[(x*2)+(y*8):((x+1)*2)+(y*8)],2)
                self.image[cur_y+y_offset+y][cur_x+x_offset+x] = np.append(RGB[idx], A[idx])
    def cmpr_tile(self, tile_data, cur_x, cur_y):
        # tile_data : 32B, 4 sub-tiles, 64 texels
        # handle sub-tiles
        x_offset = 0
        y_offset = 0
        for subtile_i in range(0,4):
            subtile_data = tile_data[subtile_i*8:(subtile_i+1)*8]
            self.cmpr_subtile(subtile_data, x_offset, y_offset, cur_x, cur_y)
            x_offset = x_offset + 4
            if x_offset >= 8:
                x_offset = 0
                y_offset = 4
    def cmpr(self, image_tag):
        cur_x = 0
        cur_y = 0
        bytes_read = 0
        while bytes_read < image_tag.length:
            tile_data = image_tag.binary_data[bytes_read:bytes_read+32]
            self.cmpr_tile(tile_data, cur_x, cur_y)
            cur_x = cur_x + 8
            if cur_x >= self.size[0]:
                cur_x = 0
                cur_y = cur_y + 8
            bytes_read += 32   
    def texure2img(self):
        if any(v is None for v in [self.name, self.fmt, self.size, self.image]):
            print("TXTR data is missing sections")
        img = {}
        img["name"] = self.name
        img["data"] = self.image
        return img

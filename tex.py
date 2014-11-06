import struct
import sys
import tag
import texture
from PIL import Image
from PIL import ImageOps
import os

class Tex:
    tagtree = None
    texture_set = None
    def __init__(self, root_tag):
        if root_tag.type != b"TEX ":
            raise Exception("File is not a valid TEX file!")
        self.tagtree = root_tag
        self.texture_set = []
        for subtag in self.tagtree.subtags:
            if subtag.type == b"SCEN": # Mesh set
                for tset_tag in subtag.subtags:
                    for txtr_tag in tset_tag.subtags:
                        self.texture_set.append(texture.Texture(txtr_tag))
    def tex2img(self):
        imgs = []
        for texture in self.texture_set:
            tex = texture.texure2img()
            imgs.append(tex)
        return imgs
        
# If called as script, write img file for each texture
if __name__ == "__main__":
    fh = open(sys.argv[1], "rb")
    if (len(sys.argv[1]) > 4 and sys.argv[1][-3:] == "tex") and not os.path.exists(sys.argv[1][:-4]):
        os.makedirs(sys.argv[1][:-4])
    tagroot = tag.Tag(fh)
    tex = Tex(tagroot)
    imgs = tex.tex2img()
    for img in imgs:
        oimg = Image.fromarray(img["data"], 'RGBA')
        oimg = ImageOps.flip(oimg)
        oimg.save("%s/%s.png" % (sys.argv[1][:-4], img["name"]))
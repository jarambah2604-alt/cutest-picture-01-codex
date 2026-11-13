#!/usr/bin/env python3
"""Procedurally draw a moon-bunny cuddling a little star; stdlib only."""
import os
import struct
import zlib

W = H = 600
pixels = bytearray(W * H * 3)


def put(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        pixels[i:i + 3] = bytes(color)


def ellipse(cx, cy, rx, ry, color):
    x0, x1 = max(0, int(cx-rx)), min(W-1, int(cx+rx))
    y0, y1 = max(0, int(cy-ry)), min(H-1, int(cy+ry))
    for y in range(y0, y1+1):
        yy = ((y + .5 - cy) / ry) ** 2
        for x in range(x0, x1+1):
            if ((x + .5 - cx) / rx) ** 2 + yy <= 1:
                put(x, y, color)


def polygon(points, color):
    x0=max(0,int(min(x for x,y in points))); x1=min(W-1,int(max(x for x,y in points)))
    y0=max(0,int(min(y for x,y in points))); y1=min(H-1,int(max(y for x,y in points)))
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            inside=False; px=x+.5; py=y+.5; j=len(points)-1
            for i,(ax,ay) in enumerate(points):
                bx,by=points[j]
                if (ay>py)!=(by>py) and px < (bx-ax)*(py-ay)/(by-ay)+ax: inside=not inside
                j=i
            if inside: put(x,y,color)


def line(x1,y1,x2,y2,r,color):
    steps=max(1,int(max(abs(x2-x1),abs(y2-y1))))
    for i in range(steps+1):
        t=i/steps; ellipse(x1+(x2-x1)*t,y1+(y2-y1)*t,r,r,color)


def draw():
    # A quiet indigo night with a layered lavender moon halo.
    for y in range(H):
        t=y/(H-1); c=(int(25+14*t),int(35+13*t),int(78+23*t))
        for x in range(W): put(x,y,c)
    for r,col in [(218,(39,54,105)),(188,(47,65,121)),(157,(56,76,135))]: ellipse(300,278,r,r,col)
    # Little pinprick stars and soft four-point twinkles.
    for x,y,s in [(94,116,7),(478,107,6),(514,267,5),(92,354,5),(171,211,3),(432,365,4),(392,116,3),(127,262,3)]:
        ellipse(x,y,s,s,(186,220,247))
        polygon([(x,y-s*1.8),(x+s*.5,y),(x,y+s*1.8),(x-s*.5,y)],(218,235,255))
    ellipse(303,493,125,22,(28,42,90))
    # Ears, plush body, arms and round head.
    ellipse(235,170,48,116,(250,231,213)); ellipse(365,166,48,117,(250,231,213))
    ellipse(239,165,25,83,(238,164,181)); ellipse(361,161,25,84,(238,164,181))
    ellipse(222,144,7,55,(255,247,229)); ellipse(348,138,7,55,(255,247,229))
    ellipse(215,422,42,48,(247,226,206)); ellipse(228,410,40,44,(82,100,159))
    ellipse(300,399,116,119,(250,231,213)); ellipse(300,381,76,82,(255,242,222))
    ellipse(215,347,43,64,(250,231,213)); ellipse(385,347,43,64,(250,231,213))
    ellipse(300,274,151,140,(255,237,218)); ellipse(267,164,71,10,(255,247,232))
    # Star glow and a bright, simple five-point cuddle prize.
    for r,c in [(87,(108,96,155)),(72,(151,124,162)),(57,(255,205,117))]: ellipse(390,361,r,r,c)
    star=[(390,301),(405,342),(449,344),(415,371),(427,414),(390,389),(353,414),(365,371),(331,344),(375,342)]
    polygon(star,(255,218,127))
    polygon([(386,316),(396,348),(430,349),(405,367),(415,398),(390,379),(365,398),(375,367),(350,349),(381,348)],(255,237,166))
    # Paws overlap the star, making the hug unmistakable.
    ellipse(347,368,31,24,(255,242,222)); ellipse(414,375,29,24,(255,242,222))
    ellipse(345,362,8,5,(255,255,242)); ellipse(407,368,8,5,(255,255,242))
    # Oversized glossy eyes, blush, tiny nose and sleepy curved smile.
    for ex in (255,345):
        ellipse(ex,274,22,30,(58,56,91)); ellipse(ex-3,270,7,10,(255,255,244)); ellipse(ex+7,282,4,5,(177,190,226))
    ellipse(221,312,19,10,(246,166,177)); ellipse(379,312,19,10,(246,166,177))
    ellipse(300,300,8,6,(202,125,143)); line(300,305,300,312,2,(133,89,116))
    line(300,312,291,319,2,(133,89,116)); line(291,319,284,315,2,(133,89,116))
    line(300,312,309,319,2,(133,89,116)); line(309,319,316,315,2,(133,89,116))
    for x,y in [(229,310),(239,317),(361,317),(371,310)]: ellipse(x,y,2,2,(238,130,157))
    polygon([(405,348),(409,359),(420,361),(409,364),(405,375),(402,364),(391,361),(402,359)],(255,255,225))


def chunk(kind, data):
    body=kind+data
    return struct.pack('>I',len(data))+body+struct.pack('>I',zlib.crc32(body)&0xffffffff)


def main():
    draw()
    raw=b''.join(b'\0'+bytes(pixels[y*W*3:(y+1)*W*3]) for y in range(H))
    image=(b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+
           chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b''))
    out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output')
    os.makedirs(out,exist_ok=True)
    with open(os.path.join(out,'entry.png'),'wb') as f: f.write(image)


if __name__ == '__main__':
    main()

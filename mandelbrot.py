from tkinter import *
from tkinter import filedialog as fd
from time import time
import re
from threading import Thread


XM, YM = 800, 600
MAX_ITER = 100
BASE_SIZE = XM / 4
INIT_MODE = 2
scale = 0


def size1(s):
    return BASE_SIZE * 10 ** (s)


s1 = size1(scale)

px0, py0 = 3 * XM / 5, YM / 2

point_r = 3
pointer = 0

cx, cy = XM / 2, YM / 2


def mandelbrot(c):
    z = c
    i = 0
    while i < MAX_ITER and abs(z) < 2:
        z = z ** 2 + c
        i += 1
    return i


def rgb(r, g, b):
    return '#{:03x}{:03x}{:03x}'.format(int(0xfff * r), int(0xfff * g), int(0xfff * b))


def color_pal(level):
    L = 5 * level
    if L < 1:
        return rgb(L, 0, 0)
    elif L < 2:
        return rgb(2 - L, L - 1, 0)
    elif L < 3:
        return rgb(0, 3 - L, L - 2)
    elif L < 5:
        return rgb((L - 3) / 2, (L - 3) / 2, 1)
    else:
        return rgb(1, 1, 1)


def color_gray(level):
    return rgb(level, level, level)


def color_black(level):
    if level > 0:
        return rgb(1, 1, 1)
    else:
        return rgb(0, 0, 0)


def dec_x(i):
    return (i - px0) / s1


def dec_y(j):
    return (py0 - j) / s1


root = Tk()
root.title('Set of Malderbrot')
root.resizable(0, 0)
cn = Canvas(root, width=XM, height=YM, bg='white')
cn.pack()

pinfo = Frame(root, bg='white', height=20, relief='raise')
info = Label(pinfo, bg='white')

img = PhotoImage(width=XM, height=YM)


def draw():
    global img

    act['state'] = DISABLED

    if rb_state.get() == 1:
        color = color_black
    elif rb_state.get() == 2:
        color = color_gray
    else:
        color = color_pal

    info['text'] = 'Calculate...'
    t0 = time()
    cn.update()
    per = 0

    tmp_img = PhotoImage(width=XM, height=YM)
    tmp_img.blank()

    for i in range(XM):
        per2 = 100 * i // XM
        if per2 != per:
            per = per2
            info['text'] = 'Processing: {:3}%'.format(per)
            info.update()
        for j in range(YM):
            c = complex(dec_x(i), dec_y(j))
            tmp_img.put(color(1 - mandelbrot(c) / MAX_ITER), to=(i, j))

    cn.delete('all')
    img = tmp_img.copy()
    cn.create_image(0, 0, anchor=NW, image=img)
    cn.create_line(0, py0, XM, py0, arrow=LAST)
    cn.create_line(px0, YM, px0, 0, arrow=LAST)

    info['text'] = 'Size: {}x{}; Iter: {}; Time: {:2f} c; (x={}, y={}); Width: {}'.format(XM, YM, MAX_ITER, time() - t0,
                                                                                          dec_x(XM / 2), dec_y(YM / 2),
                                                                                          YM / s1)

    act['state'] = NORMAL


pn = Frame(height=60)
pn.pack(fill='x')


def cn_clisk(event):
    i, j = event.x, event.y
    global pointer
    if (pointer > 0):
        cn.delete(pointer)
    pointer = cn.create_oval(i - point_r, j - point_r, i + point_r, j + point_r, fill='yellow', outline='red', tag='p')
    print(i, j)
    global cx, cy
    cx, cy = i, j


cn.bind('<Button-1>', cn_clisk)

ent_scale = Entry(pn, width=8)
ent_iter = Entry(pn, width=8)


def action():
    global s1, px0, py0, MAX_ITER, scale, cx, cy
    s2 = size1(float(ent_scale.get()))
    px0 = XM / 2 - s2 * (cx - px0) / s1
    py0 = YM / 2 + s2 * (py0 - cy) / s1
    s1 = s2
    MAX_ITER = int(ent_iter.get())
    cx, cy = XM / 2, YM / 2
    draw()
    # Thread(target=draw).start()


act = Button(pn, text='Redraw', command=action)
act.pack(side=LEFT, padx=10)

Label(pn, text='  Scale:').pack(side=LEFT)

ent_scale.pack(side=LEFT)
ent_scale.insert(0, str(scale))

Label(pn, text='  Iter: ').pack(side=LEFT)
ent_iter.pack(side=LEFT)
ent_iter.insert(0, str(MAX_ITER))


def save():
    fn = fd.asksaveasfilename(initialdir='.', title='Save picture', filetypes=(('PNG file', '*.png'),))
    print(fn)
    if fn:
        if not re.search(r'\.png', fn, re.I):
            fn += '.png'
        img.write(fn, format='png')
        print('Save to file: {}'.format(fn))
    else:
        print('Cancel')


sv = Button(pn, text='Save', command=save)

chouse_color = LabelFrame(pn, text='Color Type')
chouse_color.pack(side=LEFT, padx=20)

rb_state = IntVar()
rb_state.set(INIT_MODE)


rb1 = Radiobutton(chouse_color, text='Black', indicatoron=0, variable=rb_state, value=1)
rb2 = Radiobutton(chouse_color, text='Gray', indicatoron=0, variable=rb_state, value=2)
rb3 = Radiobutton(chouse_color, text='Color', indicatoron=0, variable=rb_state, value=3)
rb1.pack(side=LEFT)
rb2.pack(side=LEFT)
rb3.pack(side=LEFT)

sv.pack(side=LEFT)

pinfo.pack(fill=X)
info.pack(side=LEFT)
info['text'] = 'Hello!'

root.after(0, draw)
# Thread(target=draw).start()


root.mainloop()

import wx
import numpy as np
from road_damage_detective import *


class OtherFrame(wx.Frame):
    # 初始化
    def __init__(self, parent, id, title, result):
        # 继承父类的__init__()函数
        wx.Frame.__init__(self, parent, id, title, size=(1100, 600))
        self.result = result
        self.title = title
        self.list=['无','竖向裂缝   ','横向裂缝   ','地面龟裂   ','坑洼         ','斑马线模糊','白线模糊   ']
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self, -1, size=(1100, 600))
        sizer = wx.BoxSizer(wx.HORIZONTAL)  # 列间隔为10，行间隔为20
        # panel.SetBackgroundColour('yellow')

        btn1 = wx.Button(panel, -1, '角度1')
        sizer.Add(btn1, proportion=0, flag=wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.change_picture1, btn1)
        btn2 = wx.Button(panel, -1, '角度2')
        sizer.Add(btn2, proportion=0, flag=wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.change_picture2, btn2)
        btn3 = wx.Button(panel, -1, '角度3')
        sizer.Add(btn3, proportion=0, flag=wx.ALL, border=5)
        self.Bind(wx.EVT_BUTTON, self.change_picture3, btn3)

        v_sizer = wx.BoxSizer(wx.VERTICAL)
        # Imfor = wx.TextCtrl(panel, size=(283, 600))
        v_sizer.Add(sizer, proportion=0, flag=wx.EXPAND)
        s0='检测到地面异常数量为： '+str(self.result[0][3])
        self.text0 = wx.StaticText(parent=panel, label=s0)
        v_sizer.Add(self.text0, proportion=0, flag=wx.ALL, border=5)

        # text.SetForegroundColour("Black")
        # text.SetBackgroundColour("White")
        s = "   "
        if self.result[0][3]>0:
            s = '具体信息如下'
            for i in range(self.result[0][3]):
                s = s + '\n'+ self.list[self.result[0][2][i]] + '        概率为：' + str(self.result[0][1][i])

        self.text1 = wx.StaticText(parent=panel, label=s)
        v_sizer.Add(self.text1, proportion=0, flag=wx.ALL, border=5)

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_file = 'predict_image\\0.jpg'
        image1 = wx.Image(image_file, wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        self.bmp = wx.StaticBitmap(panel, -1, image1)  # 转化为.StaticBitmap()形式
        h_sizer.Add(v_sizer, proportion=0, flag=wx.EXPAND)
        h_sizer.Add(self.bmp, proportion=0, flag=wx.ALL, border=5)
        # 将Panmel适应GridBagSizer()放置
        self.SetSizer(h_sizer)

    def change_picture1(self, event):
        if self.title == "0号点":
            s0='检测到地面异常数量为： '+str(self.result[0][3])
            self.text0.SetLabel(s0)
            s = "   "
            if self.result[0][3] > 0:
                s = '具体信息如下'
                for i in range(self.result[0][3]):
                    s = s + '\n' + self.list[self.result[0][2][i]] + '        概率为：' + str(self.result[0][1][i])
            self.text1.SetLabel(s)
            image = wx.Image('predict_image\\0.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        elif self.title == "1号点":
            image = wx.Image('predict_image\\1.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        elif self.title == "2号点":
            image = wx.Image('predict_image\\2.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        self.bmp.SetBitmap(wx.BitmapFromImage(image))

    def change_picture2(self, event):
        if self.title == "0号点":
            s0 = '检测到地面异常数量为： ' + str(self.result[1][3])
            self.text0.SetLabel(s0)
            s = "   "
            if self.result[1][3] > 0:
                s = '具体信息如下'
                for i in range(self.result[1][3]):
                    s = s + '\n' + self.list[self.result[1][2][i]] + '        概率为：' + str(self.result[1][1][i])
            self.text1.SetLabel(s)
            image = wx.Image('predict_image\\1.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        elif self.title == "1号点":
            image = wx.Image('predict_image\\2.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        elif self.title == "2号点":
            image = wx.Image('predict_image\\0.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        self.bmp.SetBitmap(wx.BitmapFromImage(image))

    # 定义文字及图片转换函数
    def change_picture3(self, event):
        # 将文字“北京”换成“广州”
        # self.text2.SetLabel("广州")
        # 获取广州的图片，转化为Bitmap形式
        if self.title == "0号点":
            s0 = '检测到地面异常数量为： ' + str(self.result[2][3])
            self.text0.SetLabel(s0)
            s = "   "
            if self.result[2][3] > 0:
                s = '具体信息如下'
                for i in range(self.result[2][3]):
                    s = s + '\n' + self.list[self.result[2][2][i]] + '        概率为：' + str(self.result[2][1][i])
            self.text1.SetLabel(s)
            image = wx.Image('predict_image\\2.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        elif self.title == "1号点":
            image = wx.Image('predict_image\\1.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        elif self.title == "2号点":
            image = wx.Image('predict_image\\2.jpg', wx.BITMAP_TYPE_ANY).Rescale(800, 600).ConvertToBitmap()
        # 更新GridBagSizer()的self.bmp2
        self.bmp.SetBitmap(wx.BitmapFromImage(image))


def show_other0(event):
    frame = OtherFrame(None, -1, "0号点", result_decoded)
    frame.Show()


def show_other1(event):
    result_decoded1 = [(np.array([0, 697, 587, 879]), np.array([60, 668, 1009, 915]), np.array([0.3550625, 0.30893087]),
                        np.array([1, 1]), 2),
                       (np.array([0, 697, 587, 879]), np.array([60, 668, 1009, 915]), np.array([0.3550625, 0.30893087]),
                        np.array([1, 1]), 2),
                       (np.array([0, 697, 587, 879]), np.array([60, 668, 1009, 915]), np.array([0.3550625, 0.30893087]),
                        np.array([1, 1]), 2)]
    frame = OtherFrame(None, -1, "1号点", result_decoded1)
    frame.Show()


def show_other2(event):
    result_decoded2 = [(np.array([0, 697, 587, 879]), np.array([60, 668, 1009, 915]), np.array([0.3550625, 0.30893087]),
                        np.array([1, 1]), 2),
                       (np.array([0, 697, 587, 879]), np.array([60, 668, 1009, 915]), np.array([0.3550625, 0.30893087]),
                        np.array([1, 1]), 2),
                       (np.array([0, 697, 587, 879]), np.array([60, 668, 1009, 915]), np.array([0.3550625, 0.30893087]),
                        np.array([1, 1]), 2)]
    frame = OtherFrame(None, -1, "2号点", result_decoded2)
    frame.Show()
    # f2 = wx.Frame(None, -1, size=(800,600))
    #
    # ch1 = wx.ComboBox(panel, -1, value='C#', choices=list1)
    # self.Bind(wx.EVT_COMBOBOX, self.on_combox, ch1)
    # hbox1.Add(statictext, 1, flag=wx.LEFT | wx.RIGHT | wx.FIXED_MINSIZE)
    # hbox1.Add(ch1, 1, flag=wx.ALL | wx.EXPAND)
    # Cho = wx.Choice(f2, -1, (100, 50), choices=['左边', '前方', '右方'])
    # f2.Show()


result_decoded = image_predict()

level = 0
color = ["file\\green", "file\\green", "file\\green"]
for i in range(3):
    if result_decoded[i][3] > 0:
        level = result_decoded[i][1].sum()
        if level > 0.5:
            color[0] = "file\\red"
            break
        elif 0 < level <= 0.5:
            color[0] = "file\\yellow"

app = wx.App()
win = wx.Frame(None, title="RoadDamageDetector", size=(1010, 575))
win.Show()
image_file = 'file\\image.jpg'
to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
win.bitmap = wx.StaticBitmap(win, -1, to_bmp_image, (0, 0))
image_width = to_bmp_image.GetWidth()
image_height = to_bmp_image.GetHeight()

s0 = color[0] + ".bmp"
bmp0 = wx.Image(s0, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
button0 = wx.BitmapButton(win.bitmap, -1, bmp0, pos=(450, 170), size=(10, 10))
s1 = color[1] + ".bmp"
bmp1 = wx.Image(s1, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
button1 = wx.BitmapButton(win.bitmap, -1, bmp1, pos=(500, 100), size=(10, 10))
s2 = color[2] + ".bmp"
bmp2 = wx.Image(s2, wx.BITMAP_TYPE_BMP).ConvertToBitmap()
button2 = wx.BitmapButton(win.bitmap, -1, bmp2, pos=(450, 300), size=(10, 10))

button0.Bind(wx.EVT_BUTTON, show_other0)
button1.Bind(wx.EVT_BUTTON, show_other1)
button2.Bind(wx.EVT_BUTTON, show_other2)

win.Show()
app.MainLoop()

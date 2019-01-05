# -*- coding: utf-8 -*-
import wx,os
import wx.lib.imagebrowser as imagebrowser
import urllib2
from PIL import Image,ImageEnhance
from pytesser import *
      
class MyFrame(wx.Frame):
    def __init__(self):
        Path = os.path.dirname(os.path.realpath(__file__))
    
        wx.Frame.__init__(self, None, -1, u"第8次上机练习(WX)", size=(900, 600))
        icon = wx.Icon(name=Path + "\\icon1.ICO", type=wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        
        self.image = 0
        self.isimage = 0
        self.bmpSizeX1, self.bmpSizeY1 = 0, 0
        self.bmp1 = None
        self.road = ''
        self.result = ''
        
        self.w1 = 0
        self.h1 = 0
    
        self.menuBar = wx.MenuBar()
    
        self.panel=wx.Panel(self)
        self.SetBackgroundColour("Light Grey") 
        font = wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.text = wx.StaticText(self, -1, u"图像文件:None", pos=(10,10))
        self.text.SetFont(font)
        
        font2 = wx.Font(50, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.text2 = wx.StaticText(self, -1, u"", pos=(50,100))
        self.text2.SetFont(font2)
    
        self.statusbar = self.CreateStatusBar()
    
        File = wx.Menu()
        Open = wx.NewId()
        File.Append(Open, u"打开(&O)\tCtrl+O", u"Open Image File")
        self.Bind(wx.EVT_MENU, self.OnOpen, id=Open)
        Download = wx.NewId()
        File.Append(Download, u"下载验证码(&D)\tCtrl+D", u"Download Captcha")
        self.Bind(wx.EVT_MENU, self.OnDownload, id=Download)
        File.Append(201, u"保存(&S)\tCtrl+S", u"Save Text File")
        self.Bind(wx.EVT_MENU, self.OnSave, id=201)
        Exit = wx.NewId()
        File.Append(Exit, u"退出(&X)\tCtrl+X", u"Exit")
        self.Bind(wx.EVT_MENU, self.OnClose, id=Exit)
        self.menuBar.Append(File, u"文件(&F)")
        self.menuBar.Enable(201, False)

        OCR = wx.Menu()
        English = wx.NewId()
        OCR.Append(English, u"识别英文(&E)\tCtrl+E", u"Recognize as English")
        self.Bind(wx.EVT_MENU, self.OnEnglish, id=English)
        Chinese = wx.NewId()
        OCR.Append(Chinese, u"识别中文(&Z)\tCtrl+Z", u"Recognize as Simplified Chinese")
        self.Bind(wx.EVT_MENU, self.OnChinese, id=Chinese)
        self.menuBar.Append(OCR, u"OCR(&T)")
    
        Picture = wx.Menu()
        Enhance = wx.NewId()
        Picture.Append(Enhance, u"图像增强(&W)\tCtrl+W", u"Image Enhance")
        self.Bind(wx.EVT_MENU, self.OnEnhance, id=Enhance)
        self.menuBar.Append(Picture, u"图像(&I)")

        menu = wx.Menu()
        IdAbout = menu.Append(-1, u"程序信息(&I)\tF1", u"Program Info")
        self.Bind(wx.EVT_MENU, self.OnHelp, IdAbout)
        self.menuBar.Append(menu, u"关于(&A)")
        self.SetMenuBar(self.menuBar)
    
        self.Bind(wx.EVT_PAINT, self.OnPaint)
  
  
    def OnOpen(self, evt):
        path = os.path.dirname(os.path.realpath(__file__))
        dialog = imagebrowser.ImageDialog(self, path)
        if dialog.ShowModal() == wx.ID_OK:
            self.image = wx.Image(name = dialog.GetFile(), type=wx.BITMAP_TYPE_ANY)
            if self.image:
                self.bmp1 = self.image.ConvertToBitmap()
                self.bmpSizeX1, self.bmpSizeY1 = self.bmp1.GetWidth(), self.bmp1.GetHeight()
                self.isimage = 1
                self.road = dialog.GetFile()
                self.text.SetLabel(u"图像文件：" + self.road)
            else:
                wx.MessageBox(u"图像文件不正确",u"ERROR", wx.OK | wx.ICON_INFORMATION, self)
                self.isimage = 0
                self.road = ''
                self.text.SetLabel(u"图像文件：None")
            self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Refresh()
        dialog.Destroy()
        self.menuBar.Enable(201, False)
           
    def OnDownload(self, evt):
        url = 'https://portal1.ecnu.edu.cn/cas/Captcha.jpg'
        path = os.path.dirname(os.path.realpath(__file__))
        self.road = path + '/testFiles/captcha.jpg'
        im = open(self.road, "wb")
        im.write(urllib2.urlopen(url).read())
        im.close()
        self.image = wx.Image(name = self.road, type=wx.BITMAP_TYPE_ANY)
        
        self.bmp1 = self.image.ConvertToBitmap()
        self.bmpSizeX1, self.bmpSizeY1 = self.bmp1.GetWidth(), self.bmp1.GetHeight()
        self.isimage = 1
        self.text.SetLabel(u"图像文件：./testFiles/captcha.jpg")
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Refresh()
        self.menuBar.Enable(201, False)
        
    def OnSave(self, evt):
        wildcard = "Text Files (*.txt)|*.txt|" \
                   "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Save textfile as...", os.getcwd(), "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            filename = u"" + dialog.GetPath()
            textfile = open(filename, 'w')
            textfile.write(self.result)
            textfile.close()
            self.menuBar.Enable(201, False)
        
        dialog.Destroy()  
           
    def OnEnglish(self, evt):
        if self.road == '':
            wx.MessageBox(u"没有打开的图像文件",u"ERROR", wx.OK | wx.ICON_INFORMATION, self)
            return
        im = Image.open(self.road)
        self.result = image_to_string(im, language = 'eng')
        self.text2.SetLabel(u"正在识别，请等待……")
        wx.MessageBox(self.result, u"TEXT", wx.OK | wx.ICON_INFORMATION, self)
        self.text2.SetLabel(u"")
        if self.result:
            self.menuBar.Enable(201, True)
           
    def OnChinese(self, evt):
        if self.road == '':
            wx.MessageBox(u"没有打开的图像文件",u"ERROR", wx.OK | wx.ICON_INFORMATION, self)
            return
        im = Image.open(self.road)
        self.result = image_to_string(im, language = 'chi_sim')
        self.text2.SetLabel(u"正在识别，请等待……")
        wx.MessageBox(self.result.decode('utf-8'), u"TEXT", wx.OK | wx.ICON_INFORMATION, self)
        self.text2.SetLabel(u"")
        if self.result:
            self.menuBar.Enable(201, True)
           
    def OnEnhance(self, evt):
        if self.road == '':
            wx.MessageBox(u"尚未装入图像文件",u"ERROR", wx.OK | wx.ICON_INFORMATION, self)
            return
        image1 = Image.open(self.road)
        enhancer = ImageEnhance.Contrast(image1)  
        image2 = enhancer.enhance(100)

        wildcard = "Bitmap Files (*.bmp)|*.bmp|" \
                   "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Save Image file as...", os.getcwd(), "", wildcard, wx.SAVE)
        if dialog.ShowModal() == wx.ID_OK:
            self.road = u"" + dialog.GetPath()
            image2.save(self.road)
            
            self.image = wx.Image(name = self.road, type=wx.BITMAP_TYPE_BMP)
        
            self.bmp1 = self.image.ConvertToBitmap()
            self.bmpSizeX1, self.bmpSizeY1 = self.bmp1.GetWidth(), self.bmp1.GetHeight()
            self.isimage = 1
            self.text.SetLabel(u"图像文件：" + self.road)
            self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        dialog.Destroy()  
        self.Refresh()
        self.menuBar.Enable(201, False)

    def OnHelp(self, evt):
        wx.MessageBox(u"第8次上机练习(WX)\n图片转换成文本\n\n学号：10152130122\n姓名：钱庭涵\n",
           u"WXLab8", wx.OK | wx.ICON_INFORMATION, self)
	
    def OnClose(self, evt):
        self.Close()
        
    def OnPaint(self, evt):
                
        dc0 = wx.ClientDC(self)
        dc0.SetPen(wx.Pen("Light Grey"))
        
        dc0.DrawLine(10,30,self.w1,30)
        dc0.DrawLine(10,30,10,self.h1)
        dc0.DrawLine(10,self.h1,self.w1,self.h1)
        dc0.DrawLine(self.w1,30,self.w1,self.h1)
        
        self.w1 = self.GetClientSize().GetWidth() - 10
        self.h1 = self.GetClientSize().GetHeight() - 10
        
        dc = wx.ClientDC(self)
        
        dc.DrawLine(10,30,self.w1,30)
        dc.DrawLine(10,30,10,self.h1)
        dc.DrawLine(10,self.h1,self.w1,self.h1)
        dc.DrawLine(self.w1,30,self.w1,self.h1)
        
        dc2 = wx.PaintDC(self)
        
        dc2.DrawLine(10,30,self.w1,30)
        dc2.DrawLine(10,30,10,self.h1)
        dc2.DrawLine(10,self.h1,self.w1,self.h1)
        dc2.DrawLine(self.w1,30,self.w1,self.h1)
        
        if self.isimage == 1:
            dc1 = wx.PaintDC(self)
            dcMem1 = wx.MemoryDC()
            dcMem1.SelectObject(self.bmp1)
            dc1.Blit(15, 35, self.bmpSizeX1, self.bmpSizeY1, dcMem1, 0, 0, wx.COPY)

if __name__ == u'__main__':
  app = wx.PySimpleApp()
  frame = MyFrame()
  frame.Show(True)
  app.MainLoop()
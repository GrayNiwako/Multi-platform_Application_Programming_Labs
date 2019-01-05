# -*- coding: utf-8 -*-
import wx,os

class SubclassDialog1(wx.Dialog):
  def __init__(self):
    wx.Dialog.__init__(self, None, -1, u'复选显示位图选择',size=(300, 200))
    okButton = wx.Button(self, wx.ID_OK, u"确定", pos=(160, 30))
    okButton.SetDefault()
    cancelButton = wx.Button(self, wx.ID_CANCEL, u"取消",pos=(160, 100))
    frame.check1 = wx.CheckBox(self, -1, u"复选位图1", (50,30), (100,30))
    frame.check2 = wx.CheckBox(self, -1, u"复选位图2", (50,70), (100,30))
    frame.check3 = wx.CheckBox(self, -1, u"复选位图3", (50,110), (100,30))
    if frame.FuXuanWeiTu1 == 1:
        frame.check1.SetValue(True)
    else:
        frame.check1.SetValue(False)
    if frame.FuXuanWeiTu2 == 1:
        frame.check2.SetValue(True)
    else:
        frame.check2.SetValue(False)
    if frame.FuXuanWeiTu3 == 1:
        frame.check3.SetValue(True)
    else:
        frame.check3.SetValue(False)

class SubclassDialog2(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self, parent, -1, u'单选显示位图选择',size=(300, 200))
    okButton = wx.Button(self, wx.ID_OK, u"确定", pos=(160, 30))
    okButton.SetDefault()
    cancelButton = wx.Button(self, wx.ID_CANCEL, u"取消",pos=(160, 100))
    self.Bind(wx.EVT_BUTTON, frame.OnOK, okButton)
    self.Bind(wx.EVT_BUTTON, frame.OnCancel, cancelButton)
    frame.radio1 = wx.RadioButton(self, -1, u"单选位图1", (50,30), style=wx.RB_GROUP)
    frame.radio2 = wx.RadioButton(self, -1, u"单选位图2", (50,70))
    frame.radio3 = wx.RadioButton(self, -1, u"单选位图3", (50,110))
    if frame.DaXuanWeiTu1 == 1:
        frame.radio1.SetValue(True)
    if frame.DaXuanWeiTu2 == 1:
        frame.radio2.SetValue(True)
    if frame.DaXuanWeiTu3 == 1:
        frame.radio3.SetValue(True)
    
class MyFrame(wx.Frame):
  def __init__(self):
    Path = os.path.dirname(os.path.realpath(__file__))
    
    wx.Frame.__init__(self, None, -1, u"第6次上机练习(WX)", size=(800, 500))
    icon = wx.Icon(name=Path + "\\icon1.ICO", type=wx.BITMAP_TYPE_ICO)
    self.SetIcon(icon)
    cursor = wx.StockCursor(wx.CURSOR_ARROW)
    self.SetCursor(cursor)
    self.menuBar = wx.MenuBar()
    
    self.panel=wx.Panel(self)
    self.SetBackgroundColour("Light Grey") 
    self.text = wx.StaticText(self, -1, u"当前光标是：ARROW", pos=(10,10))
    
    self.lan = 1
    self.cur = 1
    self.FuXuanWeiTu1 = 0
    self.FuXuanWeiTu2 = 0
    self.FuXuanWeiTu3 = 0
    self.DaXuanWeiTu1 = 1
    self.DaXuanWeiTu2 = 0
    self.DaXuanWeiTu3 = 0
    
    File = wx.Menu()
    Exit = wx.NewId()
    File.Append(Exit, u"退出(&x)")
    self.Bind(wx.EVT_MENU, self.OnClose, id=Exit)
    self.menuBar.Append(File, u"文件(&F)")
    
    IdDialog = wx.Menu()
    ModelDialog = wx.NewId()
    IdDialog.Append(ModelDialog, u"模式对话框(&M)\tCtrl+A")
    self.Bind(wx.EVT_MENU, self.OnModelDialog, id=ModelDialog)
    ModellessDialog = wx.NewId()
    IdDialog.Append(ModellessDialog, u"无模式对话框(&L)\tCtrl+B")
    self.Bind(wx.EVT_MENU, self.OnModellessDialog, id=ModellessDialog)
    FileDialog = wx.NewId()
    IdDialog.Append(FileDialog, u"文件对话框(&F)\tCtrl+C")
    self.Bind(wx.EVT_MENU, self.OnFileDialog, id=FileDialog)
    self.menuBar.Append(IdDialog, u"对话框(&D)")
    
    CursorType = wx.Menu()
    CursorType.Append(301, u"光标&1(箭头)\tCtrl+1", u"", wx.ITEM_RADIO)
    CursorType.Append(302, u"光标&2(十字)\tCtrl+2", u"", wx.ITEM_RADIO)
    CursorType.Append(303, u"光标&3(自定义)\tCtrl+3", u"", wx.ITEM_RADIO)
    self.Bind(wx.EVT_MENU_RANGE, self.OnCursor,id=301,id2=303)
    self.menuBar.Append(CursorType, u"光标类型(&C)")
    self.menuBar.Check(301,True)

    Language = wx.Menu()
    Language.Append(401, u"中文(&C)\tCtrl+Shift+C", u"", wx.ITEM_RADIO)
    Language.Append(402, u"&English\tCtrl+Shift+D", u"", wx.ITEM_RADIO)
    self.Bind(wx.EVT_MENU_RANGE, self.OnLanguage,id=401,id2=402)
    self.menuBar.Append(Language, u"语言(&L)")
    self.menuBar.Check(401,True)

    menu = wx.Menu()
    IdAbout = menu.Append(-1, u"程序信息(&I)\tF1", u"Help tip")
    self.Bind(wx.EVT_MENU, self.OnHelp, IdAbout)
    self.menuBar.Append(menu, u"关于(&A)")
    self.SetMenuBar(self.menuBar)
    
    image1 = wx.Image(name=Path + "\\1.bmp", type=wx.BITMAP_TYPE_BMP)
    self.bmp1 = image1.ConvertToBitmap()
    self.bmpSizeX1, self.bmpSizeY1 = self.bmp1.GetWidth(), self.bmp1.GetHeight()
    #self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    image2 = wx.Image(name=Path + "\\2.bmp", type=wx.BITMAP_TYPE_BMP)
    self.bmp2 = image2.ConvertToBitmap()
    self.bmpSizeX2, self.bmpSizeY2 = self.bmp2.GetWidth(), self.bmp2.GetHeight()
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    image3 = wx.Image(name=Path + "\\3.bmp", type=wx.BITMAP_TYPE_BMP)
    self.bmp3 = image3.ConvertToBitmap()
    self.bmpSizeX3, self.bmpSizeY3 = self.bmp3.GetWidth(), self.bmp3.GetHeight()
    self.Bind(wx.EVT_PAINT, self.OnPaint)
  
  def OnCursor(self, evt):
    if(evt.GetId() == 301):
        cursor = wx.StockCursor(wx.CURSOR_ARROW)
        self.SetCursor(cursor)
        self.cur = 1
        if self.lan == 1:
            self.text.SetLabel(u"当前光标是：ARROW")
        else:
            self.text.SetLabel(u"The current cursor is: ARROW")
    if(evt.GetId() == 302):
        cursor = wx.StockCursor(wx.CURSOR_CROSS)
        self.SetCursor(cursor)
        self.cur = 2
        if self.lan == 1:
            self.text.SetLabel(u"当前光标是：CROSS")
        else:
            self.text.SetLabel(u"The current cursor is: CROSS")
    if(evt.GetId() == 303):
        cursor = wx.Cursor(cursorName = os.path.dirname(os.path.realpath(__file__)) + "\\cursor1.CUR", type=wx.BITMAP_TYPE_CUR)
        self.SetCursor(cursor)
        self.cur = 3
        if self.lan == 1:
            self.text.SetLabel(u"当前光标是：我的光标")
        else:
            self.text.SetLabel(u"The current cursor is: MY CURSOR")
      
  def OnLanguage(self, evt):
    if(evt.GetId() == 402):
        self.SetTitle("Lab6(WX)")
        self.lan = 2
        
        if self.cur == 1:
            self.text.SetLabel(u"The current cursor is: ARROW")
        if self.cur == 2:
            self.text.SetLabel(u"The current cursor is: CROSS")
        if self.cur == 3:
            self.text.SetLabel(u"The current cursor is: MY CURSOR")
        
        File = wx.Menu()
        Exit = wx.NewId()
        File.Append(Exit, u"E&xit")
        self.Bind(wx.EVT_MENU, self.OnClose, id=Exit)
        self.menuBar.Replace(0, File, u"&File")
        
        IdDialog = wx.Menu()
        ModelDialog = wx.NewId()
        IdDialog.Append(ModelDialog, u"&Modal Dialog…\tCtrl+A")
        self.Bind(wx.EVT_MENU, self.OnModelDialog, id=ModelDialog)
        ModellessDialog = wx.NewId()
        IdDialog.Append(ModellessDialog, u"Modal&Less Dialog…\tCtrl+B")
        self.Bind(wx.EVT_MENU, self.OnModellessDialog, id=ModellessDialog)
        FileDialog = wx.NewId()
        IdDialog.Append(FileDialog, u"&File Dialog…\tCtrl+C")
        self.Bind(wx.EVT_MENU, self.OnFileDialog, id=FileDialog)
        self.menuBar.Replace(1, IdDialog, u"&Dialog")
        
        CursorType = wx.Menu()
        CursorType.Append(301, u"Cursor&1(ARROW)\tCtrl+1", u"", wx.ITEM_RADIO)
        CursorType.Append(302, u"Cursor&2(CROSS)\tCtrl+2", u"", wx.ITEM_RADIO)
        CursorType.Append(303, u"Cursor&3(UserDefined)\tCtrl+3", u"", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU_RANGE, self.OnCursor,id=301,id2=303)
        self.menuBar.Replace(2, CursorType, u"&Cursor")
        self.menuBar.Check(self.cur + 300,True)
        
        self.menuBar.SetMenuLabel(3, u"&Language")
        
        menu = wx.Menu()
        IdAbout = menu.Append(-1, u"Program &Information\tF1", u"Help tip")
        self.Bind(wx.EVT_MENU, self.OnHelp, IdAbout)
        self.menuBar.Replace(4, menu, u"&About")
        
    else:
        self.SetTitle(u"第6次上机练习(WX)")
        self.lan = 1
        
        if self.cur == 1:
            self.text.SetLabel(u"当前光标是：ARROW")
        if self.cur == 2:
            self.text.SetLabel(u"当前光标是：CROSS")
        if self.cur == 3:
            self.text.SetLabel(u"当前光标是：我的光标")
        
        File = wx.Menu()
        Exit = wx.NewId()
        File.Append(Exit, u"退出(&x)")
        self.Bind(wx.EVT_MENU, self.OnClose, id=Exit)
        self.menuBar.Replace(0, File, u"文件(&F)")
        
        IdDialog = wx.Menu()
        ModelDialog = wx.NewId()
        IdDialog.Append(ModelDialog, u"模式对话框(&M)\tCtrl+A")
        self.Bind(wx.EVT_MENU, self.OnModelDialog, id=ModelDialog)
        ModellessDialog = wx.NewId()
        IdDialog.Append(ModellessDialog, u"无模式对话框(&L)\tCtrl+B")
        self.Bind(wx.EVT_MENU, self.OnModellessDialog, id=ModellessDialog)
        FileDialog = wx.NewId()
        IdDialog.Append(FileDialog, u"文件对话框(&F)\tCtrl+C")
        self.Bind(wx.EVT_MENU, self.OnFileDialog, id=FileDialog)
        self.menuBar.Replace(1, IdDialog, u"对话框(&D)")
        
        CursorType = wx.Menu()
        CursorType.Append(301, u"光标&1(箭头)\tCtrl+1", u"", wx.ITEM_RADIO)
        CursorType.Append(302, u"光标&2(十字)\tCtrl+2", u"", wx.ITEM_RADIO)
        CursorType.Append(303, u"光标&3(自定义)\tCtrl+3", u"", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU_RANGE, self.OnCursor,id=301,id2=303)
        self.menuBar.Replace(2, CursorType, u"光标类型(&C)")
        self.menuBar.Check(self.cur + 300,True)
        
        self.menuBar.SetMenuLabel(3, u"语言(&L)")
        
        menu = wx.Menu()
        IdAbout = menu.Append(-1, u"程序信息(&I)\tF1", u"Help tip")
        self.Bind(wx.EVT_MENU, self.OnHelp, IdAbout)
        self.menuBar.Replace(4, menu, u"关于(&A)")

  def OnFileDialog(self, evt):
    wildcard = "Python source (*.py)|*.py|" \
                "Compiled Python (*.pyc)|*.pyc|" \
                "All files (*.*)|*.*"
    dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
    if dialog.ShowModal() == wx.ID_OK:
        Road = u"所选文件名："+dialog.GetPath()
        wx.MessageBox(Road, u"文件名", wx.OK | wx.ICON_INFORMATION, self)
    dialog.Destroy()  
    self.Refresh()
    
  def OnModelDialog(self, evt):
    dialog = SubclassDialog1()
    result = dialog.ShowModal()
    if result == wx.ID_OK:
        if self.check1.IsChecked():
            self.FuXuanWeiTu1 = 1
        else:
            self.FuXuanWeiTu1 = 0
        
        if self.check2.IsChecked():
            self.FuXuanWeiTu2 = 1
        else:
            self.FuXuanWeiTu2 = 0
        if self.check3.IsChecked():
            self.FuXuanWeiTu3 = 1
        else:
            self.FuXuanWeiTu3 = 0
    self.Bind(wx.EVT_PAINT, self.OnPaint, self)
    self.Refresh()
    dialog.Destroy()
  
  def OnModellessDialog(self, evt):
    self.dialog = SubclassDialog2(self)
    self.dialog.Show()
    
  def OnOK(self, evt):
    if self.radio1.GetValue() == True:
        self.DaXuanWeiTu1 = 1
    else:
        self.DaXuanWeiTu1 = 0
    if self.radio2.GetValue() == True:
        self.DaXuanWeiTu2 = 1
    else:
        self.DaXuanWeiTu2 = 0
    if self.radio3.GetValue() == True:
        self.DaXuanWeiTu3 = 1
    else:
        self.DaXuanWeiTu3 = 0
    self.Bind(wx.EVT_PAINT, self.OnPaint, self)
    self.Refresh()

  def OnCancel(self, evt):
    self.dialog.Destroy()
    
  def OnPaint(self,evt):
    clientSizeX1,clientSizeY1 = self.GetClientSize()
    dc1 = wx.PaintDC(self)
    dcMem1 = wx.MemoryDC()
    dcMem1.SelectObject(self.bmp1)
    if self.FuXuanWeiTu1 == 1:
        dc1.Blit(50, 50, 100, 100, dcMem1, 0, 0, wx.COPY)
    if self.DaXuanWeiTu1 == 1:
        dc1.Blit(300, 30, self.bmpSizeX1, self.bmpSizeY1, dcMem1, 0, 0, wx.COPY)
        
    clientSizeX2,clientSizeY2 = self.GetClientSize()
    dc2 = wx.PaintDC(self)
    dcMem2 = wx.MemoryDC()
    dcMem2.SelectObject(self.bmp2)
    if self.FuXuanWeiTu2 == 1:
        dc2.Blit(50, 170, 100, 100, dcMem2, 0, 0, wx.COPY)
    if self.DaXuanWeiTu2 == 1:
        dc2.Blit(300, 30, self.bmpSizeX2, self.bmpSizeY2, dcMem2, 0, 0, wx.COPY)
    
    clientSizeX3,clientSizeY3 = self.GetClientSize()
    dc3 = wx.PaintDC(self)
    dcMem3 = wx.MemoryDC()
    dcMem3.SelectObject(self.bmp3)
    if self.FuXuanWeiTu3 == 1:
        dc3.Blit(50, 290, 100, 100, dcMem3, 0, 0, wx.COPY)
    if self.DaXuanWeiTu3 == 1:
        dc3.Blit(300, 30, self.bmpSizeX3, self.bmpSizeY3, dcMem3, 0, 0, wx.COPY)

  def OnHelp(self, evt):
    wx.MessageBox(u"第6次上机练习(WX)\n对话框、光标、字符串、位图\n\n学号：10152130122\n姓名：钱庭涵\n",
           u"WXLab6", wx.OK | wx.ICON_INFORMATION, self)
	
  def OnClose(self, evt):
    self.Close()

if __name__ == u'__main__':
  app = wx.PySimpleApp()
  frame = MyFrame()
  frame.Show(True)
  app.MainLoop()
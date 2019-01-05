# -*- coding: utf-8 -*-
import wx
class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, u"第4次上机练习(WX)", size=(800, 500))
    icon = wx.Icon(name=u"D:\\TTde\\学习\\大二下\\多平台\\Lab4\\15Lab4_10152130122\\icon1.ICO", type=wx.BITMAP_TYPE_ICO)
    self.SetIcon(icon)
    self.menuBar = wx.MenuBar()
    menu = wx.Menu()
    menu.Append(wx.ID_EXIT, u"E&xit\tCtrl+Shift+Delete", u"Exit this simple sample")
    self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
    self.menuBar.Append(menu, u"&File")
    
    self.text = wx.StaticText(self, -1, u"当前使用的图标是：图标1", pos=(100,50))
    self.text1 = wx.StaticText(self, -1, u"", pos=(200,200))
    self.text2 = wx.StaticText(self, -1, u"", pos=(200,300))
    self.text3 = wx.StaticText(self, -1, u"", pos=(300,200))
    self.text4 = wx.StaticText(self, -1, u"", pos=(300,300))
    
    self.tubiao = wx.Menu()
    self.tubiao.Append(201, u"图标1\tCtrl+1", u"", wx.ITEM_RADIO)
    self.tubiao.Append(202, u"图标2\tCtrl+2", u"", wx.ITEM_RADIO)
    self.tubiao.Append(203, u"图标3\tCtrl+3", u"", wx.ITEM_RADIO)
#    self.Bind(wx.EVT_MENU, self.Ontubiao,id=201)
#    self.Bind(wx.EVT_MENU, self.Ontubiao,id=202)
#    self.Bind(wx.EVT_MENU, self.Ontubiao,id=203)
    self.Bind(wx.EVT_MENU_RANGE, self.Ontubiao,id=201,id2=203)
    self.menuBar.Append(self.tubiao, u"图标(&I)")
    self.menuBar.Check(201,True)	
    self.changeable = True

    xianshi = wx.Menu()
    xianshi.Append(301, u"显示1\tCtrl+Shift+1", u"", wx.ITEM_CHECK)
    xianshi.Append(302, u"显示2\tCtrl+Shift+2", u"", wx.ITEM_CHECK)
    xianshi.Append(303, u"显示3\tCtrl+Shift+3", u"", wx.ITEM_CHECK)
    xianshi.Append(304, u"显示4\tCtrl+Shift+4", u"", wx.ITEM_CHECK)
    self.menuBar.Append(xianshi, u"显示(&D)")
    self.Bind(wx.EVT_MENU, self.Onxianshi,id=301,id2=304)

    menu = wx.Menu()
    IdAbout = menu.Append(-1, u"程序信息(&I)\tF1", u"Help tip")
    self.Bind(wx.EVT_MENU, self.OnHelp, IdAbout)
    self.menuBar.Append(menu, u"关于(&A)")
    self.SetMenuBar(self.menuBar)

  def Ontubiao(self, evt):
    item = self.GetMenuBar().FindItemById(evt.GetId())
    text = item.GetText()
    wx.MessageBox(u"确定要修改吗？", u"Confirmation", wx.YES_NO | wx.ICON_QUESTION, self)
    if self.changeable:
      Road = u"D:\\TTde\\学习\\大二下\\多平台\\Lab4\\15Lab4_10152130122\\icon" + text[-1] + ".ICO"
      icon = wx.Icon(name=Road, type=wx.BITMAP_TYPE_ICO)
      self.SetIcon(icon)
      Word = u"当前使用的图标是：图标" + text[-1]
      self.text.SetLabel(Word)
    if text[-1] == '3':
        self.MenuBar.EnableTop(2, False)
    else:
        self.MenuBar.EnableTop(2, True)
	 
  def Onxianshi(self, evt):
    item_2 = self.GetMenuBar().FindItemById(evt.GetId())
    text_2 = item_2.GetText()
    if text_2[-1] == '1':
        if evt.IsChecked():
            self.text1.SetLabel(text_2)
        else:
            self.text1.SetLabel(u"")
    if text_2[-1] == '2':
        if evt.IsChecked():
            self.text2.SetLabel(text_2)
        else:
            self.text2.SetLabel(u"")
    if text_2[-1] == '3':
        if evt.IsChecked():
            self.text3.SetLabel(text_2)
        else:
            self.text3.SetLabel(u"")
    if text_2[-1] == '4':
        if evt.IsChecked():
            self.text4.SetLabel(text_2)
        else:
            self.text4.SetLabel(u"")

  def OnHelp(self, evt):
    wx.MessageBox(u"第4次上机练习(WX)\n图标、菜单、加速键、消息框\n\n学号：10152130122\n姓名：钱庭涵\n",
           u"Lab4(WX)", wx.OK | wx.ICON_INFORMATION, self)
	
  def OnClose(self, evt):
    self.Close()

if __name__ == u'__main__':
  app = wx.PySimpleApp()
  frame = MyFrame()
  frame.Show(True)
  app.MainLoop()
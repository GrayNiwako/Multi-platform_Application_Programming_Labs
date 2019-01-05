# -*- coding: utf8 -*- 
import wx 
import psutil
class MyFrame(wx.Frame):
  def __init__(self):
    wx.Frame.__init__(self, None, -1, "My Frame", size=(800, 600))
    panel = wx.Panel(self, -1)
    wx.StaticText(panel, -1, u"进程ID：    模块名：", pos=(10, 20))
    wx.StaticText(panel, -1, u"进程ID：    模块名：", pos=(310, 20))
    wx.StaticText(panel, -1, u"进程ID：    模块名：", pos=(610, 20))
    ACCESS_DENIED=''
    i=0
    for pid in sorted(psutil.pids()):
      try:
        p = psutil.Process(pid)
        pinfo = p.as_dict(ad_value=ACCESS_DENIED)
        wx.StaticText(panel, -1, u"%05x      %s"%(pid,pinfo['name']), pos=(10+300*(i%3), 20+20*((i+3)/3)))
        i+=1
      except psutil.NoSuchProcess: pass
if __name__ == '__main__':
  app = wx.PySimpleApp()
  frame = MyFrame()
  frame.Show(True)
  app.MainLoop()


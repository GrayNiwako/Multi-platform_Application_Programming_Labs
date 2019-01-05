#!/usr/bin/python
# -*- coding: utf8 -*-

# snake.py

import wx
import random

class Snake(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(900, 700))
        
        self.menuBar = wx.MenuBar()
        
        self.RemPaused = 0
        self.GameStart = 0
        self.GameModel = 1
        
        IdAbout = wx.Menu()
        Start = wx.NewId()
        IdAbout.Append(Start, u"开始(&S)\tS")
        self.Bind(wx.EVT_MENU, self.OnStart, id=Start)
        
        ReStart = wx.NewId()
        IdAbout.Append(ReStart, u"重新开始(&R)\tR")
        self.Bind(wx.EVT_MENU, self.OnReStart, id=ReStart)
        
        Instruction = wx.NewId()
        IdAbout.Append(Instruction, u"操作说明(&E)\tF1")
        self.Bind(wx.EVT_MENU, self.OnInstruction, id=Instruction)
        
        Information = wx.NewId()
        IdAbout.Append(Information, u"程序信息(&I)\tF2")
        self.Bind(wx.EVT_MENU, self.OnInformation, id=Information)
        
        Exit = wx.NewId()
        IdAbout.Append(Exit, u"退出(&X)\tEsc")
        self.Bind(wx.EVT_MENU, self.OnClose, id=Exit)
        self.menuBar.Append(IdAbout, u"关于(&A)")
        
        IdModel =wx.Menu()
        IdModel.Append(201, u"简单(&1)\tCtrl+1", u"", wx.ITEM_RADIO)
        IdModel.Append(202, u"正常(&2)\tCtrl+2", u"", wx.ITEM_RADIO)
        IdModel.Append(203, u"困难(&3)\tCtrl+3", u"", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU_RANGE, self.OnModel,id=201,id2=203)
        self.menuBar.Append(IdModel, u"难易度(&M)")
        self.menuBar.Check(201, True)
        
        self.SetMenuBar(self.menuBar)
        
        self.initFrame()
        
        wx.MessageBox(u"S/s   :  开始\nR/r  ： 重新开始\nP/p  ： 暂停\nD/d  ： 加速\n",
           u"操作说明", wx.OK | wx.ICON_INFORMATION, self)
    
    def initFrame(self):
        
        self.initpos = 700
        self.sp = wx.SplitterWindow(self)
        self.sp.statusbar = self.CreateStatusBar()
        self.sp.statusbar.SetStatusText('0')
        self.board = Board(self.sp, style = wx.SUNKEN_BORDER)
        self.record = Record(self.sp, style = wx.SUNKEN_BORDER)
        self.record.SetBackgroundColour("White")
        self.sp.SplitVertically(self.board, self.record, self.initpos)
        
        self.board.SetFocus()

        self.Centre()
        self.Show(True)
        
    def OnStart(self, evt):
        self.board.start()
        self.GetMenuBar().Enable(evt.GetId(), False)
        self.GameStart = 1
        
    def OnReStart(self, evt):
        if self.GameStart == 1:
            self.board.initBoard()
            statusbar = self.sp.statusbar
            statusbar.SetStatusText('0')
            self.record.score.SetLabel(u"0")
            self.board.start()
           
    def OnInstruction(self, evt):
        if self.board.isPaused == True:
            self.RemPaused = 1
        else:
            self.RemPaused = 0
            
        if self.RemPaused == 0:
            self.board.pause()
        
        wx.MessageBox(u"S/s   :  开始\nR/r  ： 重新开始\nP/p  ： 暂停\nD/d  ： 加速\n",
           u"操作说明", wx.OK | wx.ICON_INFORMATION, self)
           
        if self.RemPaused == 0:
            self.board.pause()
            
    def OnInformation(self, evt):
        if self.board.isPaused == True:
            self.RemPaused = 1
        else:
            self.RemPaused = 0
            
        if self.RemPaused == 0:
            self.board.pause()
        
        wx.MessageBox(u"第7次上机练习(WX)\n贪吃蛇\n\n学号：10152130122\n姓名：钱庭涵\n",
           u"15Lab7(WX)", wx.OK | wx.ICON_INFORMATION, self)
           
        if self.RemPaused == 0:
            self.board.pause()
       
    def OnClose(self, evt):
        self.Close()
        
    def OnModel(self, evt):
        if evt.GetId() == 201:
            Board.Speed = 300
            self.GameModel = 1
        if evt.GetId() == 202:
            Board.Speed = 200
            self.GameModel = 2
        if evt.GetId() == 203:
            Board.Speed = 100
            self.GameModel = 3

class Board(wx.Panel):
    
    BoardWidth = 30
    BoardHeight = 30
    Speed = 100
    ID_TIMER = 1
    NotExist = 0
    IsExist = 1
    IsFoodExist = 2

    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.initBoard()
        
    def initBoard(self):    

        self.timer = wx.Timer(self, Board.ID_TIMER)
        self.isWaiting = False
        self.curHeadX = Board.BoardWidth / 2
        self.curHeadY = Board.BoardHeight / 2
        self.curTailX = Board.BoardWidth / 2 - 1
        self.curTailY = Board.BoardHeight / 2
        self.length = 2
        self.curFoodX = 0
        self.curFoodY = 0
        self.curDirection = 'Right'
        self.EatNumber = 0
        
        self.board = [[Board.NotExist for col in range(Board.BoardHeight)] for row in range(Board.BoardWidth)]
        self.board[self.curHeadY][self.curHeadY] = Board.IsExist
        self.board[self.curTailY][self.curTailY] = Board.IsExist
        
        self.roadX = [0 for i in range(Board.BoardWidth)]
        self.roadY = [0 for i in range(Board.BoardWidth)]
        self.roadX[0] = self.curHeadX
        self.roadY[0] = self.curHeadY
        self.roadX[1] = self.curTailX
        self.roadY[1] = self.curTailY

        self.isStarted = False
        self.isPaused = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        self.clearBoard()

    def start(self):
        
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaiting = False
        self.EatNumber = 0
        self.clearBoard()

        self.timer.Start(Board.Speed)

    def pause(self):
        
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused
        statusbar = self.GetParent().statusbar

        if self.isPaused:
            self.timer.Stop()
            statusbar.SetStatusText('paused')
        else:
            self.timer.Start(Board.Speed)
            statusbar.SetStatusText(str(self.EatNumber))

        self.Refresh()

    def clearBoard(self):
        
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Board.NotExist)

    def OnErase(self, event):
        1 == 1

    def OnPaint(self, event):

        dc = wx.BufferedPaintDC(self)

        size = self.GetClientSize()
        
        dc.SetPen(wx.ThePenList.FindOrCreatePen("Light Grey", 1, wx.SOLID))
        dc.DrawRectangle(0, 0, size.GetWidth(), size.GetHeight())
        
        for i in range(Board.BoardWidth):
            for j in range(Board.BoardHeight):
                if self.board[i][j] == Board.IsExist:
                    dc.SetBrush(wx.Brush(colour=wx.BLACK, style=wx.BRUSHSTYLE_SOLID))
                    dc.DrawRectangle(i * (900 / Board.BoardWidth), j * (900 / Board.BoardHeight), 900 / Board.BoardWidth, 900 / Board.BoardHeight)
                elif self.board[i][j] == Board.IsFoodExist:
                    dc.SetBrush(wx.Brush(colour=wx.RED, style=wx.BRUSHSTYLE_SOLID))
                    dc.DrawRectangle(i * (900 / Board.BoardWidth), j * (900 / Board.BoardHeight), 900 / Board.BoardWidth, 900 / Board.BoardHeight)
        

    def OnKeyDown(self, event):

        if not self.isStarted:
            event.Skip()
            return

        keycode = event.GetKeyCode()

        if keycode == ord('P') or keycode == ord('p'):
            self.pause()
            return
        if self.isPaused:
            return
        elif keycode == wx.WXK_LEFT:
            if self.curDirection[0] != 'r':
                self.tryMove('left')
        elif keycode == wx.WXK_RIGHT:
            if self.curDirection[0] != 'l':
                self.tryMove('right')
        elif keycode == wx.WXK_DOWN:
            if self.curDirection[0] != 'u':
                self.tryMove('down')
        elif keycode == wx.WXK_UP:
            if self.curDirection[0] != 'd':
                self.tryMove('up')
        elif keycode == ord('D') or keycode == ord('d'):
            self.tryMove(self.curDirection)
        else:
            event.Skip()


    def OnTimer(self, event):
        
        if event.GetId() == Board.ID_TIMER:
            if self.isWaiting:
                self.isWaiting = False
                self.CreateFood()
            else:
                event.Skip()
        else:
            event.Skip()


    def CreateFood(self):
        
        statusbar = self.GetParent().statusbar
        
        self.curFoodX = random.randint(0, Board.BoardWidth - 1)
        self.curFoodY = random.randint(0, Board.BoardHeight - 1)
        while self.board[self.curFoodY][self.curFoodY] == Board.IsExist:
            if self.EatNumber == 898:
                break
            self.curFoodX = random.randint(0, Board.BoardWidth - 1)
            self.curFoodY = random.randint(0, Board.BoardHeight - 1)
        if self.EatNumber !=898 :
           self.board[self.curFoodY][self.curFoodY] = Board.IsFoodExist

        if not self.tryMove(self.curDirection):
            
            self.timer.Stop()
            self.isStarted = False
            self.CurrentScore = self.EatNumber
            
            if self.GetParent().GetParent().GameModel == 1:
                self.BestScore = int(self.GetParent().GetParent().record.score1.GetLabel())
                if self.CurrentScore > self.BestScore:
                    self.BestScore = self.CurrentScore
                    self.GetParent().GetParent().record.score1.SetLabel(str(self.BestScore))
                    wx.MessageBox(u"恭喜你！突破了简单模式的记录！",
                       u"Congratulation", wx.OK | wx.ICON_INFORMATION, self)
                    
            if self.GetParent().GetParent().GameModel == 2:
                self.BestScore = int(self.GetParent().GetParent().record.score2.GetLabel())
                if self.CurrentScore > self.BestScore:
                    self.BestScore = self.CurrentScore
                    self.GetParent().GetParent().record.score2.SetLabel(str(self.BestScore))
                    wx.MessageBox(u"恭喜你！突破了正常模式的记录！",
                       u"Congratulation", wx.OK | wx.ICON_INFORMATION, self)
                    
            if self.GetParent().GetParent().GameModel == 3:
                self.BestScore = int(self.GetParent().GetParent().record.score3.GetLabel())
                if self.CurrentScore > self.BestScore:
                    self.BestScore = self.CurrentScore
                    self.GetParent().GetParent().record.score3.SetLabel(str(self.BestScore))
                    wx.MessageBox(u"恭喜你！突破了困难模式的记录！",
                       u"Congratulation", wx.OK | wx.ICON_INFORMATION, self)
                
            statusbar.SetStatusText('Game over')

    def tryMove(self, nextDirection):
        
        statusbar = self.GetParent().statusbar
        
        if nextDirection[0] == 'r':
            x = self.curHeadX + 1
            y = self.curHeadY
        elif nextDirection[0] == 'l':
            x = self.curHeadX - 1
            y = self.curHeadY
        elif nextDirection[0] == 'u':
            x = self.curHeadX
            y = self.curHeadY - 1
        else:
            x = self.curHeadX
            y = self.curHeadY + 1
            
        if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
            return False
                
        if self.board[x][y] == Board.IsExist:
            return False
        elif self.board[x][y] == Board.NotExist:
            self.board[x][y] = Board.IsExist
            self.board[self.curTailX][self.curTailY] = Board.NotExist
            for i in range(1, self.length)[::-1]:
                self.roadX[i] = self.roadX[i-1]
                self.roadY[i] = self.roadY[i-1]
            self.roadX[0] = x
            self.roadY[0] = y
            self.curHeadX = x
            self.curHeadY = y
            print '(',x,',',y,')'
            self.curTailX = self.roadX[self.length - 1]
            self.curTailY = self.roadY[self.length - 1]
            self.Refresh()
        else:
            self.board[x][y] = Board.IsExist
            self.length = self.length + 1
            self.EatNumber = self.EatNumber + 1
            for i in range(1, self.length)[::-1]:
                self.roadX[i] = self.roadX[i-1]
                self.roadY[i] = self.roadY[i-1]
            self.roadX[0] = x
            self.roadY[0] = y
            self.curHeadX = x
            self.curHeadY = y
            print '(',x,',',y,')'
            statusbar.SetStatusText(str(self.EatNumber))
            self.GetParent().GetParent().record.score.SetLabel(str(self.EatNumber))
            self.isWaiting = True 
            self.Refresh()
            
        if nextDirection[0] == 'r':
            self.curDirection = 'right'
        elif nextDirection[0] == 'l':
            self.curDirection = 'left'
        elif nextDirection[0] == 'u':
            self.curDirection = 'up'
        else:
            self.curDirection = 'down'
       

class Record(wx.Panel):
    
    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        
        self.initRecord()
        
    def initRecord(self): 
        
        font1 = wx.Font(15, wx.SWISS, wx.NORMAL,wx.BOLD)
        font2 = wx.Font(15, wx.SWISS, wx.NORMAL,wx.NORMAL)
        self.text1 = wx.StaticText(self, -1, u"当前得分：", pos=(20,100))
        self.text1.SetFont(font1)
        self.text2 = wx.StaticText(self, -1, u"最高得分：", pos=(20,300))
        self.text2.SetFont(font1)
        self.text3 = wx.StaticText(self, -1, u"简单：", pos=(20,370))
        self.text3.SetFont(font2)
        self.text4 = wx.StaticText(self, -1, u"正常：", pos=(20,440))
        self.text4.SetFont(font2)
        self.text5 = wx.StaticText(self, -1, u"困难：", pos=(20,510))
        self.text5.SetFont(font2)
        
        self.score = wx.StaticText(self, -1, u"0", pos=(80,170))
        self.score.SetFont(font1)
        self.score1 = wx.StaticText(self, -1, u"0", pos=(110,370))
        self.score1.SetFont(font1)
        self.score2 = wx.StaticText(self, -1, u"0", pos=(110,440))
        self.score2.SetFont(font1)
        self.score3 = wx.StaticText(self, -1, u"0", pos=(110,510))
        self.score3.SetFont(font1)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, event):

        dc = wx.BufferedPaintDC(self)  
        
        dc.SetPen(wx.ThePenList.FindOrCreatePen("Light Grey", 1, wx.SOLID))
        dc.DrawRectangle(0, 0, self.GetClientSize().GetWidth(), self.GetClientSize().GetHeight())


app = wx.App()
Snake(None, title=u"15Lab7 贪吃蛇")
app.MainLoop()
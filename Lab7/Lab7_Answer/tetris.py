#!/usr/bin/python
# -*- coding: utf8 -*-

# tetris.py

import wx
import random

class Tetris(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600, 700))
        
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
        
        wx.MessageBox(u"S/s      :  开始\nR/r     ： 重新开始\nP/p     ： 暂停\nSpace ： 快速降落\nD/d    ： 加速降落\n",
           u"操作说明", wx.OK | wx.ICON_INFORMATION, self)
    
    def initFrame(self):
        
        self.initpos = 340
        self.sp = wx.SplitterWindow(self)
        self.sp.statusbar = self.CreateStatusBar()
        self.sp.statusbar.SetStatusText('0')
        self.board = Board(self.sp, style = wx.SUNKEN_BORDER)
        self.record = Record(self.sp, style = wx.SUNKEN_BORDER)
        self.record.SetBackgroundColour("White")
        self.sp.SplitVertically(self.board, self.record, self.initpos)
        
        self.NextTetrisPiece = Shape()
        
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
        
        wx.MessageBox(u"S/s      :  开始\nR/r     ： 重新开始\nP/p     ： 暂停\nSpace ： 快速降落\nD/d    ： 加速降落\n",
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
        
        wx.MessageBox(u"第7次上机练习(WX)\n俄罗斯方块\n\n学号：10152130122\n姓名：钱庭涵\n",
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
    
    BoardWidth = 12
    BoardHeight = 22
    Speed = 300
    ID_TIMER = 1

    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.initBoard()
        
    def initBoard(self):    

        self.timer = wx.Timer(self, Board.ID_TIMER)
        self.isWaitingAfterLine = False
        self.curPiece = Shape()
        self.nextPiece = Shape()
        self.nextPiece.setRandomShape()
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.isStarted = False
        self.isPaused = False

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_TIMER, self.OnTimer, id=Board.ID_TIMER)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)

        self.clearBoard()

    def shapeAt(self, x, y):
        
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        
        return self.GetClientSize().GetWidth() / Board.BoardWidth

    def squareHeight(self):
        
        return self.GetClientSize().GetHeight() / Board.BoardHeight

    def start(self):
        
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.newPiece()
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
            statusbar.SetStatusText(str(self.numLinesRemoved))

        self.Refresh()

    def clearBoard(self):
        
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoes.NoShape)
            
    def OnErase(self, event):
        1 == 1

    def OnPaint(self, event):

        dc = wx.BufferedPaintDC(self)

        size = self.GetClientSize()
        boardTop = size.GetHeight() - Board.BoardHeight * self.squareHeight()
        
        dc.SetPen(wx.ThePenList.FindOrCreatePen("Light Grey", 1, wx.SOLID))
        dc.DrawRectangle(0, 0, size.GetWidth(), size.GetHeight())

        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)
                if shape != Tetrominoes.NoShape:
                    self.drawSquare(dc,
                        0 + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(dc, 0 + x * self.squareWidth(),
                    boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                    self.curPiece.shape())


    def OnKeyDown(self, event):

        if not self.isStarted or self.curPiece.shape() == Tetrominoes.NoShape:
            event.Skip()
            return

        keycode = event.GetKeyCode()

        if keycode == ord('P') or keycode == ord('p'):
            self.pause()
            return
        if self.isPaused:
            return
        elif keycode == wx.WXK_LEFT:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif keycode == wx.WXK_RIGHT:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif keycode == wx.WXK_DOWN:
            self.tryMove(self.curPiece.rotatedRight(), self.curX, self.curY)
        elif keycode == wx.WXK_UP:
            self.tryMove(self.curPiece.rotatedLeft(), self.curX, self.curY)
        elif keycode == wx.WXK_SPACE:
            self.dropDown()
        elif keycode == ord('D') or keycode == ord('d'):
            self.oneLineDown()
        else:
            event.Skip()


    def OnTimer(self, event):
        
        if event.GetId() == Board.ID_TIMER:
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
        else:
            event.Skip()


    def dropDown(self):
        
        newY = self.curY
        
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):
                break
            newY -= 1

        self.pieceDropped()

    def oneLineDown(self):
        
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()
            

    def pieceDropped(self):
        
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()


    def removeFullLines(self):
    
        numFullLines = 0

        statusbar = self.GetParent().statusbar

        rowsToRemove = []

        for i in range(Board.BoardHeight):
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoes.NoShape:
                    n = n + 1

            if n == 12:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))

            numFullLines = numFullLines + len(rowsToRemove)

            if numFullLines > 0:
                self.numLinesRemoved = self.numLinesRemoved + numFullLines
                statusbar.SetStatusText(str(self.numLinesRemoved))
                self.GetParent().GetParent().record.score.SetLabel(str(self.numLinesRemoved)) 
                self.isWaitingAfterLine = True
                self.curPiece.setShape(Tetrominoes.NoShape)
                self.Refresh()


    def newPiece(self):
        
        statusbar = self.GetParent().statusbar
        
        self.curPiece.setShape(self.nextPiece.shape())
        self.nextPiece = Shape()
        self.nextPiece.setRandomShape()
        
        self.GetParent().GetParent().NextTetrisPiece = self.nextPiece
        self.GetParent().GetParent().record.Refresh()
        
        self.curX = Board.BoardWidth / 2 + 1
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()

        if not self.tryMove(self.curPiece, self.curX, self.curY):
            
            self.curPiece.setShape(Tetrominoes.NoShape)
            self.timer.Stop()
            self.isStarted = False
            self.CurrentScore = self.numLinesRemoved
            
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
            

    def tryMove(self, newPiece, newX, newY):
        
        for i in range(4):
            
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)
            
            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False
            if self.shapeAt(x, y) != Tetrominoes.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.Refresh()
        
        return True


    def drawSquare(self, dc, x, y, shape):
        
        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']

        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC', 
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80', 
                 '#80803B', '#803B80', '#3B8080', '#806200']

        pen = wx.ThePenList.FindOrCreatePen(light[shape], 1, wx.SOLID)
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + self.squareHeight() - 1, x, y)
        dc.DrawLine(x, y, x + self.squareWidth() - 1, y)

        darkpen = wx.ThePenList.FindOrCreatePen(dark[shape], 1, wx.SOLID)
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        dc.DrawLine(x + self.squareWidth() - 1, 
        y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.TheBrushList.FindOrCreateBrush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, self.squareWidth() - 2, 
        self.squareHeight() - 2)


class Record(wx.Panel):
    
    def __init__(self, parent, style):
        wx.Panel.__init__(self, parent, style=wx.WANTS_CHARS)
        
        self.initRecord()
        
    def initRecord(self): 
        
        font1 = wx.Font(18, wx.SWISS, wx.NORMAL,wx.BOLD)
        font2 = wx.Font(15, wx.SWISS, wx.NORMAL,wx.BOLD)
        font3 = wx.Font(15, wx.SWISS, wx.NORMAL,wx.NORMAL)
        self.text1 = wx.StaticText(self, -1, u"下一个方块是：", pos=(20,20))
        self.text1.SetFont(font1)
        self.text2 = wx.StaticText(self, -1, u"当前得分：", pos=(20,300))
        self.text2.SetFont(font2)
        self.text3 = wx.StaticText(self, -1, u"最高得分：", pos=(20,400))
        self.text3.SetFont(font2)
        self.text4 = wx.StaticText(self, -1, u"简单：", pos=(20,450))
        self.text4.SetFont(font3)
        self.text5 = wx.StaticText(self, -1, u"正常：", pos=(20,500))
        self.text5.SetFont(font3)
        self.text6 = wx.StaticText(self, -1, u"困难：", pos=(20,550))
        self.text6.SetFont(font3)
        
        font4 = wx.Font(15, wx.SWISS, wx.NORMAL,wx.BOLD)
        self.score = wx.StaticText(self, -1, u"0", pos=(120,350))
        self.score.SetFont(font4)
        self.score1 = wx.StaticText(self, -1, u"0", pos=(120,450))
        self.score1.SetFont(font4)
        self.score2 = wx.StaticText(self, -1, u"0", pos=(120,500))
        self.score2.SetFont(font4)
        self.score3 = wx.StaticText(self, -1, u"0", pos=(120,550))
        self.score3.SetFont(font4)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        
    def OnPaint(self, event):

        dc = wx.BufferedPaintDC(self)  
        
        dc.SetPen(wx.ThePenList.FindOrCreatePen("Light Grey", 1, wx.SOLID))
        dc.DrawRectangle(0, 0, self.GetClientSize().GetWidth(), self.GetClientSize().GetHeight())
        
        if self.GetParent().GetParent().NextTetrisPiece.shape() != Tetrominoes.NoShape:
            for i in range(4):
                x = self.GetParent().GetParent().NextTetrisPiece.x(i)
                y = self.GetParent().GetParent().NextTetrisPiece.y(i)
                self.drawSquare(dc, 100 + x * 30, 100 + y * 30,
                    self.GetParent().GetParent().NextTetrisPiece.shape())
            
            
    def drawSquare(self, dc, x, y, shape):
        
        colors = ['#000000', '#CC6666', '#66CC66', '#6666CC',
                  '#CCCC66', '#CC66CC', '#66CCCC', '#DAAA00']

        light = ['#000000', '#F89FAB', '#79FC79', '#7979FC', 
                 '#FCFC79', '#FC79FC', '#79FCFC', '#FCC600']

        dark = ['#000000', '#803C3B', '#3B803B', '#3B3B80', 
                 '#80803B', '#803B80', '#3B8080', '#806200']

        pen = wx.ThePenList.FindOrCreatePen(light[shape], 1, wx.SOLID)
        pen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(pen)

        dc.DrawLine(x, y + 30 - 1, x, y)
        dc.DrawLine(x, y, x + 30 - 1, y)

        darkpen = wx.ThePenList.FindOrCreatePen(dark[shape], 1, wx.SOLID)
        darkpen.SetCap(wx.CAP_PROJECTING)
        dc.SetPen(darkpen)

        dc.DrawLine(x + 1, y + 30 - 1,x + 30 - 1, y + 30 - 1)
        dc.DrawLine(x + 30 - 1, y + 30 - 1, x + 30 - 1, y + 1)

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.TheBrushList.FindOrCreateBrush(colors[shape]))
        dc.DrawRectangle(x + 1, y + 1, 30 - 2, 30 - 2)


class Tetrominoes(object):
    
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


class Shape(object):
    
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        
        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Tetrominoes.NoShape

        self.setShape(Tetrominoes.NoShape)

    def shape(self):
        
        return self.pieceShape

    def setShape(self, shape):
        
        table = Shape.coordsTable[shape]
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        
        self.setShape(random.randint(1, 7))

    def x(self, index):
        
        return self.coords[index][0]

    def y(self, index):
        
        return self.coords[index][1]

    def setX(self, index, x):
        
        self.coords[index][0] = x

    def setY(self, index, y):
        
        self.coords[index][1] = y

    def minX(self):
        
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        
        m = self.coords[0][1]
        
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotatedLeft(self):
        
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        
        for i in range(4):
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

    def rotatedRight(self):
        
        if self.pieceShape == Tetrominoes.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        
        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


app = wx.App()
Tetris(None, title=u"15Lab7 俄罗斯方块")
app.MainLoop()
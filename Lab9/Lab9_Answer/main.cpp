#if defined(UNICODE) && !defined(_UNICODE)
    #define _UNICODE
#elif defined(_UNICODE) && !defined(UNICODE)
    #define UNICODE
#endif

#include <tchar.h>

#include<windows.h>
#include<stdlib.h>
#include<string.h>

LRESULT CALLBACK WndProc(HWND hWnd,UINT iMessage,UINT wParam,LONG lParam);
BOOL InitWindowsClass(HINSTANCE hInstance);
BOOL InitWindows(HINSTANCE hInstance,int nCmdShow);

BOOL InitWindowsClass(HINSTANCE hInstance)//��ʼ��������
{
		WNDCLASS WndClass;
		WndClass.cbClsExtra=0;
		WndClass.cbWndExtra=0;
		WndClass.hbrBackground=(HBRUSH)(GetStockObject(WHITE_BRUSH));
		WndClass.hCursor=LoadCursor(NULL,IDC_ARROW);
		WndClass.hIcon=LoadIcon(NULL,"END");
		WndClass.hInstance=hInstance;
		WndClass.lpfnWndProc=WndProc;
		WndClass.lpszClassName="WinText";
		WndClass.lpszMenuName=NULL;
		WndClass.style=CS_HREDRAW|CS_VREDRAW;
		return RegisterClass(&WndClass);
}

BOOL InitWindows(HINSTANCE hInstance,int nCmdShow) //��ʼ������
{
	HWND hWnd;
		hWnd=CreateWindow("WinText",  //���ɴ���
						"Lab9(SDK)",
						WS_OVERLAPPEDWINDOW,
						CW_USEDEFAULT,
						0,
						CW_USEDEFAULT,
						0,
						NULL,
						NULL,
						hInstance,
						NULL);
		if(!hWnd)
			return FALSE;
		ShowWindow(hWnd,nCmdShow);//��ʾ����
		UpdateWindow(hWnd);
		return TRUE;
}
//������
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,LPSTR lpCmdLine, int nCmdShow)
{
	MSG Message;
	if(!InitWindowsClass(hInstance))		return FALSE;
	if(!InitWindows(hInstance,nCmdShow))	return FALSE;
	while(GetMessage(&Message,0,0,0))		//��Ϣѭ��
		{TranslateMessage(&Message);
		 DispatchMessage(&Message);
        }
	return Message.wParam;
}

LRESULT CALLBACK WndProc(HWND hWnd,UINT iMessage,UINT wParam,LONG lParam)
{ static long nXChar,nCaps,nYChar;
  int pointx,pointy,i,j;
  HDC hDC;   					//����ָ���豸�����ľ��
  TEXTMETRIC tm;				//�������������ԵĽṹ�����
  PAINTSTRUCT PtStr; 			//ָ�������ͼ��Ϣ�Ľṹ�����
  const TCHAR *textbuf[4]={"�������ǻƺ�¥", "�̻�����������","�·�ԶӰ�̿վ�", "Ψ�����������"};

  CHOOSEFONT cf;            // common dialog box structure
  static LOGFONT lf;        // logical font structure
  static COLORREF rgbCurrent;  // current text color

  switch(iMessage)  					//������Ϣ
  {	case WM_CREATE:						//�����ڴ�����Ϣ

     hDC=GetDC(hWnd) ;   				//��ȡ��ǰ�豸����
	 GetTextMetrics(hDC,&tm); 			//��ȡ������Ϣ
	 nXChar=tm.tmAveCharWidth;  			//��ȡ�ַ����
     nYChar=tm.tmHeight+tm.tmExternalLeading;	//�ַ��߶�
	 nCaps=(tm.tmPitchAndFamily&1?3:2)*nXChar/2;	//�ּ��

     // Initialize CHOOSEFONT
     ZeroMemory(&cf, sizeof(cf));
     cf.lStructSize = sizeof (cf);
     cf.hwndOwner = hWnd;
     cf.lpLogFont = &lf;
     cf.rgbColors = rgbCurrent;
     cf.Flags = CF_SCREENFONTS | CF_EFFECTS;

     if (ChooseFont(&cf)==TRUE)
     {
         InvalidateRect(hWnd, NULL, TRUE);
     }
     rgbCurrent= cf.rgbColors;

	 ReleaseDC(hWnd,hDC); return 0;		//�ͷŵ�ǰ�豸���
	case WM_PAINT: 						//�����ػ���Ϣ
	 hDC=BeginPaint(hWnd,&PtStr); 		//��ʼ��ͼ

	 SelectObject(hDC, CreateFontIndirect(&lf));
     SetTextColor(hDC, rgbCurrent);

	 for(i=4;i>0;i--)
	 {for(j=0;j<7;j++)					//����ı�
        {  pointx=100+i*nXChar*12;	pointy=50+j*(nYChar+nCaps)*2;
	       TextOut(hDC,pointx,pointy,textbuf[4-i]+j*2,2);
	    }
	 }
     EndPaint(hWnd,&PtStr);
	 DeleteObject(SelectObject(hDC, GetStockObject(SYSTEM_FONT)));

     return 0; 		//������ͼ
	case WM_DESTROY: //����Ӧ�ó���
	 PostQuitMessage(0);	return 0;
	default:
		return(DefWindowProc(hWnd,iMessage,wParam,lParam));
  }
}

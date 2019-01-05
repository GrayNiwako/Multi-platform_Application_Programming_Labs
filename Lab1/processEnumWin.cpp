#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <tlhelp32.h> // 声明快照函数的头文件

LRESULT CALLBACK MainWndProc(HWND,UINT,WPARAM,LPARAM);

BOOL InitApplication(HINSTANCE);
BOOL InitInstance(HINSTANCE,int);

int WINAPI WinMain(HINSTANCE hInstance,                  // 入口函数
                   HINSTANCE,
                   LPSTR     lpCmdLine,
                   int       nCmdShow  )
{
    if (!InitApplication(hInstance))       // 应用初始化
        return FALSE;

    if (!InitInstance(hInstance,nCmdShow)) // 实例初始化
        return FALSE;

    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0))   // 消息循环
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return (int)msg.wParam;
}

BOOL InitApplication(HINSTANCE hInstance)   // 应用初始化
{
    WNDCLASS  wc;  // Data structure of the window class

    wc.style            = CS_HREDRAW|CS_VREDRAW;
    wc.lpfnWndProc      = (WNDPROC)MainWndProc;  // Name of the Window Function
    wc.cbClsExtra       = 0;
    wc.cbWndExtra       = 0;
    wc.hInstance        = hInstance;
    wc.hIcon            = LoadIcon (NULL, IDI_APPLICATION);
    wc.hCursor          = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground    = (HBRUSH)GetStockObject(WHITE_BRUSH);
    wc.lpszMenuName     = NULL;
    wc.lpszClassName    = TEXT("My1stWClass");  // Name of the window class

    return RegisterClass(&wc);
}

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)  // 实例初始化
{
    HWND hWnd = CreateWindow(TEXT("My1stWClass"),     // Name of the window class
                             TEXT("15Lab1：进程列表"), // Title of the window
                             WS_OVERLAPPEDWINDOW,
                             CW_USEDEFAULT,
                             CW_USEDEFAULT,
                             CW_USEDEFAULT,
                             CW_USEDEFAULT,
                             NULL,
                             NULL,
                             hInstance,
                             NULL                                        );
    if (!hWnd) return FALSE;

    ShowWindow(hWnd, nCmdShow);
    UpdateWindow(hWnd);

    return TRUE;
}

LRESULT CALLBACK MainWndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
    LPCTSTR wrong = TEXT("CreateToolhelp32Snapshot调用失败！");

    PAINTSTRUCT ps;
    HDC hdc;

    PROCESSENTRY32 pe32;
    HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    pe32.dwSize = sizeof(pe32);

    switch (message) {

        case WM_PAINT:  // 窗口客户区得刷新
        {
            hdc = BeginPaint (hWnd, &ps);
            if(hProcessSnap == INVALID_HANDLE_VALUE)
            {
                TextOut(hdc,200,100,wrong,lstrlen(wrong));
                CloseHandle(hProcessSnap);
                EndPaint (hWnd, &ps);
                return -1;
            }

            BOOL bMore = Process32First(hProcessSnap, &pe32);

            LPCTSTR title=TEXT("进程ID              模块名");
            TextOut(hdc,50,20,title,lstrlen(title));
            TextOut(hdc,350,20,title,lstrlen(title));
            TextOut(hdc,650,20,title,lstrlen(title));

            int i=0, iLength;
            while(bMore)
            {
                TCHAR szBuffer[200];
                iLength = wsprintf(szBuffer, TEXT ("%05x"), (unsigned)pe32.th32ProcessID );
                TextOut (hdc, 50+300*(i%3), 20+20*((i+3)/3), szBuffer, iLength) ;
                iLength = wsprintf(szBuffer, TEXT ("%s"), pe32.szExeFile );
                TextOut (hdc, 150+300*(i%3), 20+20*((i+3)/3), szBuffer, iLength) ;
                bMore = Process32Next(hProcessSnap, &pe32);
                i++;
            }

            CloseHandle(hProcessSnap); // 清除snapshot对象
            EndPaint (hWnd, &ps);
            return 0;
        }
        case WM_DESTROY: // 窗口关闭

            PostQuitMessage(0);

            return 0;

       default:  // 缺省消息的处理

           return DefWindowProc(hWnd, message, wParam, lParam);
   }

}

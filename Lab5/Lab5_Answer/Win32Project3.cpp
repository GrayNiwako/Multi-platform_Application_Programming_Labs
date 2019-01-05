#include "stdafx.h"
#include "resource.h"
#include <commdlg.h>

#define MAX_LOADSTRING 100

HINSTANCE hInst;
WCHAR szTitle[MAX_LOADSTRING];
WCHAR szWindowClass[MAX_LOADSTRING];
INT language = 1;
BOOL bCheck[3] = {0};
HWND hDlgLess = NULL;
INT iRadioSelector = 0;

ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);
BOOL    CALLBACK    DlgProc(HWND, UINT, WPARAM, LPARAM);
BOOL    CALLBACK    DlgLessProc(HWND, UINT, WPARAM, LPARAM);

int APIENTRY _tWinMain(HINSTANCE hInstance,
	HINSTANCE hPrevInstance,
	LPTSTR    lpCmdLine,
	int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);
	MSG msg;

	LoadStringW(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	LoadStringW(hInstance, IDC_WIN32PROJECT3, szWindowClass, MAX_LOADSTRING);
	MyRegisterClass(hInstance);

	if (!InitInstance(hInstance, nCmdShow))
		return FALSE;

    HACCEL hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_WIN32PROJECT3));

    while (GetMessage(&msg, NULL, 0, 0))
    {
		if ((IsWindow(hDlgLess)) && (IsDialogMessage(hDlgLess, &msg)))
			continue;
        if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
    }

    return (int) msg.wParam;
}

ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASS wc;

    wc.style          = CS_HREDRAW | CS_VREDRAW;
    wc.lpfnWndProc    = WndProc;
    wc.cbClsExtra     = 0;
    wc.cbWndExtra     = 0;
    wc.hInstance      = hInstance;
    wc.hIcon          = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_ICON1));
    wc.hCursor        = LoadCursor(NULL, IDC_ARROW);
    wc.hbrBackground  = (HBRUSH)(COLOR_WINDOW+1);
    wc.lpszMenuName   = MAKEINTRESOURCEW(IDC_WIN32PROJECT3);
    wc.lpszClassName  = szWindowClass;

	return RegisterClass(&wc);
}

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
	HWND hWnd;
	hInst = hInstance;

	hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
		CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);

	if (!hWnd)
		return FALSE;

	ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);

	return TRUE;
}

BOOL CALLBACK DlgProc(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	int i;
	switch (message)
	{
	case WM_INITDIALOG:
		for (i = IDC_CHECK1; i <= IDC_CHECK3; ++i)
			CheckDlgButton(hDlg, i, bCheck[i - IDC_CHECK1]);
		return TRUE;
	case WM_COMMAND:
		switch (LOWORD(wParam))
		{
		case IDOK:
			for (i = IDC_CHECK1; i <= IDC_CHECK3; ++i)
				bCheck[i - IDC_CHECK1] = IsDlgButtonChecked(hDlg, i);
		case IDCANCEL:
			EndDialog(hDlg, LOWORD(wParam));
			return TRUE;
		}
		break;
	}
	return FALSE;
}

BOOL  CALLBACK DlgLessProc(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	switch (message)
	{
	case WM_INITDIALOG:
		CheckRadioButton(hDlg, IDC_RADIO1, IDC_RADIO3, IDC_RADIO1 + iRadioSelector);
		return TRUE;
	case WM_COMMAND:
		switch (LOWORD(wParam))
		{
		case IDOK:
			iRadioSelector = 0;
			while (!IsDlgButtonChecked(hDlg, IDC_RADIO1 + iRadioSelector))
				++iRadioSelector;
			InvalidateRect(GetParent(hDlg), NULL, TRUE);
			return TRUE;
		case IDCANCEL:
			DestroyWindow(hDlgLess);
			hDlgLess = NULL;
			return TRUE;
		}
		break;
	}
	return FALSE;
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	static DWORD dwCursorMenuId;
	static DWORD dwLanguageMenuId;
	PAINTSTRUCT ps;
	HDC hdc, hdcMem;
	HMENU hMenu = GetMenu(hWnd);
	int wmId = LOWORD(wParam);
	int wmEvent = HIWORD(wParam);
	TCHAR str[100];
	HCURSOR hCursor;
	int i;
	HBITMAP hbmpOld;
	static HBITMAP hBmp[3];
	OPENFILENAME ofn;
	TCHAR szPath[MAX_LOADSTRING], szFile[MAX_LOADSTRING];

	switch (message)
	{
	case WM_CREATE:
		CheckMenuRadioItem(hMenu, ID_ARROW, ID_MYCURSOR, ID_ARROW, MF_BYCOMMAND);
		dwCursorMenuId = ID_ARROW;
		CheckMenuRadioItem(hMenu, ID_Chinese, ID_English, ID_Chinese, MF_BYCOMMAND);
		dwLanguageMenuId = ID_Chinese;
		for (i = IDB_BITMAP1; i <= IDB_BITMAP3; ++i)
			hBmp[i - IDB_BITMAP1] = LoadBitmap(hInst, MAKEINTRESOURCE(i));
		break;
	case WM_COMMAND:
		switch (wmId)
		{
		case IDM_EXIT:
			DestroyWindow(hWnd);
			break;
		case ID_MoShiDialog:
			if (IDOK == DialogBox(hInst, MAKEINTRESOURCE(IDD_CHECK), hWnd, DlgProc))
				InvalidateRect(hWnd, NULL, TRUE);
			break;
		case ID_WuMoShiDialog:
			if (!IsWindow(hDlgLess))
			{
				hDlgLess = CreateDialog(hInst, MAKEINTRESOURCE(IDD_RADIO), hWnd, DlgLessProc);
				ShowWindow(hDlgLess, SW_SHOW);
			}
			break;
		case ID_WenJianDialog:
			memset(&ofn, 0, sizeof(ofn));
			ofn.lStructSize = sizeof(ofn);
			ofn.hInstance = hInst;
			ofn.hwndOwner = hWnd;
			ofn.lpstrFilter = TEXT("All Files(*.*)\0*.*\0Text Files(*.txt)\0*.txt\0C++ Files(*.cpp)\0*.cpp\0\0");
			ofn.lpstrTitle = TEXT("打开");
			lstrcpy(szFile, TEXT(""));
			ofn.lpstrFile = szFile;
			ofn.nMaxFile = sizeof(szFile) / sizeof(TCHAR);
			GetCurrentDirectory(MAX_LOADSTRING, szPath);
			ofn.lpstrInitialDir = szPath;
			ofn.Flags = OFN_EXPLORER | OFN_FILEMUSTEXIST;

			if (GetOpenFileName(&ofn)) 
				MessageBox(hWnd, szFile, TEXT("文件名"), MB_OK | MB_ICONINFORMATION);

			break;
		case ID_ARROW:
		case ID_CROSS:
		case ID_MYCURSOR:
			if (wmId == ID_ARROW)
			{
				SetCursor(LoadCursor(NULL, IDC_ARROW));
				SetClassLong(hWnd, GCL_HCURSOR, (long)LoadCursor(NULL, IDC_ARROW));
			}
			if (wmId == ID_CROSS)
			{
				SetCursor(LoadCursor(NULL, IDC_CROSS));
				SetClassLong(hWnd, GCL_HCURSOR, (long)LoadCursor(NULL, IDC_CROSS));
			}
			if (wmId == ID_MYCURSOR)
			{
				SetCursor(LoadCursor(hInst, MAKEINTRESOURCE(IDC_CURSOR1)));
				SetClassLong(hWnd, GCL_HCURSOR, (long)LoadCursor(hInst, MAKEINTRESOURCE(IDC_CURSOR1)));
			}
			if (wmId != dwCursorMenuId)
			{		
				CheckMenuRadioItem(hMenu, ID_ARROW, ID_MYCURSOR, wmId, MF_BYCOMMAND);
				dwCursorMenuId = wmId;
				InvalidateRect(hWnd, NULL, TRUE);
			}
			break;
		case ID_Chinese:
		case ID_English:
			if (wmId != dwLanguageMenuId)
			{
				if (wmId == ID_Chinese)
				{
					language = 1;
					LoadStringW(hInst, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
					SetWindowText(hWnd, szTitle);
					hMenu = LoadMenu(hInst, MAKEINTRESOURCE(IDC_WIN32PROJECT3));
				}
				else
				{
					language = 2;
					LoadStringW(hInst, IDS_APP_TITLE1, szTitle, MAX_LOADSTRING);
					SetWindowText(hWnd, szTitle);
					hMenu = LoadMenu(hInst, MAKEINTRESOURCE(IDC_WIN32PROJECT4));
				}
				SetMenu(hWnd, hMenu);
				DrawMenuBar(hWnd);

				CheckMenuRadioItem(hMenu, ID_Chinese, ID_English, wmId, MF_BYCOMMAND);
				dwLanguageMenuId = wmId;
				CheckMenuRadioItem(hMenu, ID_ARROW, ID_MYCURSOR, dwCursorMenuId, MF_BYCOMMAND);
				
				InvalidateRect(hWnd, NULL, TRUE);
			}
			break;
		case ID_XinXi:
			MessageBox(hWnd, TEXT("第5次上机练习(SDK)\n对话框、光标、字符串、位图\n\n学号：10152130122\n姓名：钱庭涵\n"), TEXT("Lab5(SDK)"), MB_ICONINFORMATION);
			break;
		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;
	case WM_PAINT:
		hdc = BeginPaint(hWnd, &ps);
		if (dwCursorMenuId == ID_ARROW)
		{
			if (language == 1)
				LoadStringW(hInst, ID_STR1, str, MAX_LOADSTRING);
			else
				LoadStringW(hInst, ID_STR_E1, str, MAX_LOADSTRING);
		}
		if (dwCursorMenuId == ID_CROSS)
		{
			if (language == 1)
				LoadStringW(hInst, ID_STR2, str, MAX_LOADSTRING);
			else
				LoadStringW(hInst, ID_STR_E2, str, MAX_LOADSTRING);
		}
		if (dwCursorMenuId == ID_MYCURSOR)
		{
			if (language == 1)
				LoadStringW(hInst, ID_STR3, str, MAX_LOADSTRING);
			else
				LoadStringW(hInst, ID_STR_E3, str, MAX_LOADSTRING);
		}
		TextOut(hdc, 10, 10, str, lstrlen(str));

		hdcMem = CreateCompatibleDC(hdc);
		for (i = 0; i < 3; ++i)
		{
			if (bCheck[i])
			{
				hbmpOld = (HBITMAP)SelectObject(hdcMem, hBmp[i]);
				BitBlt(hdc, 70, i * 120 + 50, 100, 100, hdcMem, 0, 0, SRCCOPY);
				SelectObject(hdcMem, hbmpOld);
			}
		}
		hbmpOld = (HBITMAP)SelectObject(hdcMem, hBmp[iRadioSelector]);
		BitBlt(hdc, 400, 50, 400, 400, hdcMem, 0, 0, SRCCOPY);
		SelectObject(hdcMem, hbmpOld);

		DeleteDC(hdcMem);
		EndPaint(hWnd, &ps);
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	default:
		return DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}
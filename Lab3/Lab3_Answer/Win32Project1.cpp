#include "stdafx.h"
#include "resource.h"

HINSTANCE hInst;
TCHAR szTitle[] = TEXT("第3次上机练习(SDK)");;
TCHAR szWindowClass[] = TEXT("Win32Project1");

ATOM                MyRegisterClass(HINSTANCE hInstance);
BOOL                InitInstance(HINSTANCE, int);
LRESULT CALLBACK    WndProc(HWND, UINT, WPARAM, LPARAM);

int APIENTRY _tWinMain(HINSTANCE hInstance,
	HINSTANCE hPrevInstance,
	LPTSTR    lpCmdLine,
	int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);
	MSG msg;
	HACCEL hAccelTable;
	ACCEL  entryAccel[100];
	int   nEntryAccel;

	MyRegisterClass(hInstance);

	if (!InitInstance(hInstance, nCmdShow))
		return FALSE;

	hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_WIN32PROJECT1));
	nEntryAccel = CopyAcceleratorTable(hAccelTable, NULL, 0);
	CopyAcceleratorTable(hAccelTable, entryAccel, nEntryAccel);
	entryAccel[nEntryAccel].cmd = IDM_EXIT;
	entryAccel[nEntryAccel].fVirt = (FVIRTKEY | FCONTROL | FSHIFT);
	entryAccel[nEntryAccel].key = VK_DELETE;
	++nEntryAccel;
	DestroyAcceleratorTable(hAccelTable);
	hAccelTable = CreateAcceleratorTable(entryAccel, nEntryAccel);

	while (GetMessage(&msg, NULL, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	DestroyAcceleratorTable(hAccelTable);
	return (int)msg.wParam;
}

ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASS wc;

	wc.style = CS_HREDRAW | CS_VREDRAW;
	wc.lpfnWndProc = WndProc;
	wc.cbClsExtra = 0;
	wc.cbWndExtra = 0;
	wc.hInstance = hInstance;
	wc.hIcon = LoadIcon(hInstance, MAKEINTRESOURCE(IDI_ICON1));
	wc.hCursor = LoadCursor(NULL, IDC_ARROW);
	wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
	wc.lpszMenuName = MAKEINTRESOURCE(IDC_WIN32PROJECT1);
	wc.lpszClassName = szWindowClass;

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

BOOL ChangeIcon(HWND hWnd)
{
	return IDYES == MessageBox(hWnd, TEXT("确定要修改吗？"), TEXT("Confirmation"), MB_YESNO | MB_ICONQUESTION);
}

HICON GetIcon(DWORD dwIconMenuId, LPTSTR str)
{
	DWORD dwIconId;
	switch (dwIconMenuId)
	{
	case ID_tubiao1:
		dwIconId = IDI_ICON1;
		lstrcpy(str, TEXT("当前使用的图标是：图标 1"));
		break;
	case ID_tubiao2:
		dwIconId = IDI_ICON2;
		lstrcpy(str, TEXT("当前使用的图标是：图标 2"));
		break;
	case ID_tubiao3:
		dwIconId = IDI_ICON3;
		lstrcpy(str, TEXT("当前使用的图标是：图标 3"));
		break;
	default:
		return NULL;
	}
	return LoadIcon(hInst, MAKEINTRESOURCE(dwIconId));
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	static DWORD dwIconMenuId;
	PAINTSTRUCT ps;
	HDC hdc;
	HMENU hMenu = GetMenu(hWnd);
	int wmId = LOWORD(wParam);
	int wmEvent = HIWORD(wParam);
	HICON hIcon;
	TCHAR str[100];

	switch (message)
	{
	case WM_CREATE:
		CheckMenuRadioItem(hMenu, ID_tubiao1, ID_tubiao1, ID_tubiao1, MF_BYCOMMAND);
		dwIconMenuId = ID_tubiao1;
		{
			HMENU hSubMenu = CreatePopupMenu();
			AppendMenu(hSubMenu, MF_STRING, IDM_EXIT, TEXT("Exit\tCtrl+Shift+Delete"));
			InsertMenu(hMenu, 0, MF_BYPOSITION | MF_POPUP | MF_STRING, (UINT)hSubMenu, TEXT("&File"));
		}
		break;
	case WM_COMMAND:
		switch (wmId)
		{
		case ID_xinxi:
			MessageBox(hWnd, TEXT("第3次上机练习(SDK)\n图标、菜单、加速键、消息框\n\n学号：10152130122\n姓名：钱庭涵\n"), TEXT("Lab3(SDK)"), MB_ICONINFORMATION);
			break;
		case IDM_EXIT:
			DestroyWindow(hWnd);
			break;
		case ID_xianshi1:
		case ID_xianshi2:
		case ID_xianshi3:
		case ID_xianshi4:
			if (GetMenuState(hMenu, wmId, MF_BYCOMMAND) & MF_CHECKED)
				CheckMenuItem(hMenu, wmId, MF_UNCHECKED);
			else
				CheckMenuItem(hMenu, wmId, MF_CHECKED);
			InvalidateRect(hWnd, NULL, TRUE);
			break;
		case ID_tubiao1:
		case ID_tubiao2:
		case ID_tubiao3:
			if ((wmId != dwIconMenuId) && (ChangeIcon(hWnd)))
			{
				CheckMenuRadioItem(hMenu, ID_tubiao1, ID_tubiao3, wmId, MF_BYCOMMAND);
				dwIconMenuId = wmId;
				if (wmId == ID_tubiao3)
				{
					EnableMenuItem(hMenu, 2, MF_BYPOSITION | MF_GRAYED);
					DrawMenuBar(hWnd);
				}
				else
				{
					EnableMenuItem(hMenu, 2, MF_BYPOSITION | MF_ENABLED);
					DrawMenuBar(hWnd);
				}
				InvalidateRect(hWnd, NULL, TRUE);
			}
			break;
		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;
	case WM_PAINT:
		hdc = BeginPaint(hWnd, &ps);
		hIcon = GetIcon(dwIconMenuId, str);
		SetClassLong(hWnd, GCL_HICON, (long)(hIcon));
		TextOut(hdc, 100, 100, str, lstrlen(str));
		DrawIcon(hdc, 300, 100, hIcon);
		for (wmId = ID_xianshi1; wmId <= ID_xianshi4; ++wmId)
		{
			if (GetMenuState(hMenu, wmId, MF_BYCOMMAND) & MF_CHECKED)
				DrawIcon(hdc, 230 + (wmId - ID_xianshi1) % 2 * 100, 230 + (wmId - ID_xianshi1) / 2 * 100, hIcon);
		}
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
#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <tlhelp32.h> // 声明快照函数的头文件

int main()
{ PROCESSENTRY32 pe32;

  // 给系统内的所有进程拍快照
  HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

  // 在使用这个结构之前，先设置它的大小
  pe32.dwSize = sizeof(pe32);

  if(hProcessSnap == INVALID_HANDLE_VALUE)
  { printf("CreateToolhelp32Snapshot调用失败！\n"); return -1; }

    // 遍历进程快照，轮流显示每个进程的信息
    BOOL bMore = Process32First(hProcessSnap, &pe32);
    while(bMore)
    { printf(" 进程ID:  %05x   模块名:  %s\n", (unsigned)pe32.th32ProcessID,pe32.szExeFile);
      bMore = Process32Next(hProcessSnap, &pe32);
    }
    CloseHandle(hProcessSnap); // 清除snapshot对象
    getch(); //Press any key to end
    return 0;
}

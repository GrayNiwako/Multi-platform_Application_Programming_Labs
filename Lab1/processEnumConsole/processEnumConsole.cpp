#include <windows.h>
#include <stdio.h>
#include <conio.h>
#include <tlhelp32.h> // �������պ�����ͷ�ļ�

int main()
{ PROCESSENTRY32 pe32;

  // ��ϵͳ�ڵ����н����Ŀ���
  HANDLE hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

  // ��ʹ������ṹ֮ǰ�����������Ĵ�С
  pe32.dwSize = sizeof(pe32);

  if(hProcessSnap == INVALID_HANDLE_VALUE)
  { printf("CreateToolhelp32Snapshot����ʧ�ܣ�\n"); return -1; }

    // �������̿��գ�������ʾÿ�����̵���Ϣ
    BOOL bMore = Process32First(hProcessSnap, &pe32);
    while(bMore)
    { printf(" ����ID:  %05x   ģ����:  %s\n", (unsigned)pe32.th32ProcessID,pe32.szExeFile);
      bMore = Process32Next(hProcessSnap, &pe32);
    }
    CloseHandle(hProcessSnap); // ���snapshot����
    getch(); //Press any key to end
    return 0;
}

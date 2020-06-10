#include <stdio.h>
#include <stdlib.h>
#include <WinSock2.h>
#include <iostream>
#include <thread>
#include <mutex>
#include <process.h>
#include <fstream>
#include <errno.h>
#include <string.h>
#pragma comment(lib,"ws2_32.lib")

using namespace std;
#define  PORT  8086        //监听套接字的缺省协议端口号
#define	 QUEL  10          //监听套接字的请求队列大小
#define  MAX   4096
bool mark=0;//1:已经达到10张图片
bool pend=0;//1:读取完1张图片
int  dirname = 1;//文件夹编号
int  quence1 = 1;//文件夹1的图片存储序列
int  quence2 = 1;//
int  quence3 = 1;//
char EOF0=255;//图片结束标识符
char EOF1=217;
char recvBuf[MAX]={0};//接收缓存
char p[MAX];//存放文件路径
void Recv(SOCKET sockClient,int dirname, int& quence);
int main(int argc, char* argv[])
{
    // 加载socket动态链接库(dll)
	WORD wVersionRequested;
	WSADATA wsaData;
	char last[3]={0,0,0};
	int err;
	wVersionRequested = MAKEWORD(2, 2);//加载套接字库 版本号为2.2
	//检错
	err = WSAStartup(wVersionRequested, &wsaData);
	if ( err != 0)
	{
		cout << "error = " << err << endl;
		WSACleanup();
		return -1;
	}
	if (LOBYTE(wsaData.wVersion) != 2 || HIBYTE(wsaData.wVersion) != 2)
	{
	    // 检查是否为2.2版本
		// 否则的话，调用WSACleanup()清除信息，结束函数
		WSACleanup();
		return -1;
	}

	// 创建服务器socket，建立流式套接字，返回套接字号sockSrv
	// SOCKET socket(int af, int type, int protocol);
	// 第一个参数，指定地址簇 TCP/IP只能是AF_INET
	// 第二个，选择套接字的类型(流式套接字)，第三个，特定地址家族相关协议（0为自动）
	SOCKET sockSrv = socket(AF_INET, SOCK_STREAM, 0);
	if(sockSrv == INVALID_SOCKET)
    {
        cout<<"fail to creat socket!"<<endl;
        exit(1);
    }
	sockaddr_in addSrv; //定义本机地址信息
	addSrv.sin_family = AF_INET;
	addSrv.sin_addr.S_un.S_addr = inet_addr("192.168.137.1");// 本地回路地址是127.0.0.1;htonl(INADDR_ANY);//自动填充本地IP
	int port;
	if(argc>1)
        port = atoi(argv[1]);//如果指定了端口号，将其转换为整数
    else
        port = PORT;
    if(port>0)//测试端口号是否合法
        addSrv.sin_port = htons((short)port);//端口号转化为网络字节顺序
    else
    {
        printf("bad port number %s\n",argv[1]);
    }
    // 套接字sockSrv与本地地址相连
    // int bind(SOCKET s, const struct sockaddr* name, int namelen);
	// 第一个参数，指定需要绑定的套接字；
	// 第二个参数，指定该套接字的本地地址信息，该地址结构会随所用的网络协议的不同而不同
	// 第三个参数，指定该网络协议地址的长度
	err = bind(sockSrv, (SOCKADDR*)&addSrv, sizeof(addSrv));// 第二参数要强制类型转换
    if(err == SOCKET_ERROR)
    {
        cout<<"fail to bind!"<<endl;
        exit(1);
    }

	// 设置为监听模式（连接请求）
	// int listen(SOCKET s,  int backlog);void Recv(SOCKET sockClient)
	// 第一个参数指定需要设置的套接字，第二个参数为（等待连接队列的最大长度）
	err = listen(sockSrv, QUEL);
    if(err == SOCKET_ERROR)
    {
        cout<<"fail to listen!"<<endl;
        exit(1);
    }
	sockaddr_in addrClient;//客户端地址信息
	int len = sizeof(SOCKADDR);
    cout<<"等待连接中..."<<endl;
    while(1)
    {
        SOCKET sockClient = accept(sockSrv, (SOCKADDR*)&addrClient, &len);//创建新的套接字与当前客户端相连

        if(sockClient == SOCKET_ERROR)
            cout<<"接收错误"<<endl;
        else
        {
            printf("接收到一个连接：%s", inet_ntoa(addrClient.sin_addr));
            cout<<"------------------------------------------------------\n";
            char recvBuf[MAX]={0};
            char p[MAX];
            int  byte = 0;
            char  quence ='0';
            while(1)
            {
                switch(dirname)
                {
                    case 1: Recv(sockClient,dirname, quence1);
                            break;
                    case 2: Recv(sockClient,dirname, quence2);
                            break;
                    case 3: Recv(sockClient,dirname, quence3);
                            break;
                }
                dirname++;
                if(dirname==4)
                  dirname=1;
                Sleep(1000);
            }
            closesocket(sockClient);
            cout<<"已经断开和客户端的连接"<<endl;
            Sleep(1000);
            cout<<"------------------------------------------------------\n";
        }
    }
    closesocket(sockSrv);
    WSACleanup();// 终止对套接字库的使用
	system("pause");

	return 0;
}
//接受并存储一张图片
// sockClient：客户端套接字编号
// fname：文件夹编号
void Recv(SOCKET sockClient,int dirname, int& quence)
{
    int  byte = 0;
    sprintf(p,"save_images\\t%d\\%d.jpg",dirname,quence);
    byte = recv(sockClient, recvBuf, sizeof(recvBuf),0);//接收数据
    if(byte > 0)
    {
        cout<<"开始接收数据"<<endl;
        cout<<"TCP服务器端接收到的字节数："<<endl;
        ofstream output( p, ios::out | ios::binary );
        if( output.fail() )
        {
            printf("%s", strerror(errno));
            cout << "Open output file error!" << endl;
            exit( -1 );
        }
        for(int i=0; i<byte; i++)
        {
            output.write ((char *) &recvBuf[i], sizeof(char) );
            //printf("%c",recvBuf[i]);
        }
            while(!pend)
        {
            byte = recv(sockClient, recvBuf, sizeof(recvBuf),0);//接收数据
            printf("%d\n",byte);
            if(byte <= 0)
            continue;
            //recvBuf[byte-1];
            if((recvBuf[byte-4]==EOF0)&&(recvBuf[byte-3]==EOF1)&&(recvBuf[byte-2]==EOF0)&&(recvBuf[byte-1]==EOF1-1))
            {
                for(int i=0; i<byte-4; i++)
                {
                    output.write ((char *) &recvBuf[i], sizeof(char) );
                    //printf("%c",recvBuf[i]);
                }
                cout<<"接收完成"<<endl;
                pend=1;
                quence++;
                if(quence==11)
                    quence=1;
            }
            else
            {
                for(int i=0; i<byte; i++)
                {
                    output.write ((char *) &recvBuf[i], sizeof(char) );
                    //printf("%c",recvBuf[i]);
                }
            }
            memset(recvBuf,'\0', MAX);
        }
        output.close();
        pend=0;
    }
    //sprintf(p,"C:\\Users\\wwz\\Desktop\\Server2\\server\\bin\\Debug\\save_images\\t%d\\%d.jpg",dirname,quence);


}


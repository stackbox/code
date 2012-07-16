#include <iostream>
#include <winsock2.h>
using namespace std;


int main(int argc,char *argv[]) {
    WSADATA Ws;
    SOCKET ClientSocket;
    char* lpbuffer;

    if (WSAStartup(MAKEWORD(2,2), &Ws) != 0 )
     {
        cout<<"Init Windows Socket Failed::"<<GetLastError()<<endl;
        return -1;
     }
    char request[1024] = "GET /index.html HTTP/1.1\r\nHost:www.baidu.com\r\nConnection: Keep-Alive\r\n\r\n";
    cout << request<<endl;

    HOSTENT *host_entry = gethostbyname("www.baidu.com");
    lpbuffer = inet_ntoa(*((struct in_addr *)host_entry->h_addr)) ;
    cout << "IP ADDRESS:" << lpbuffer << endl;
    cout << "haddr1:" << host_entry->h_addr_list[0];


    sockaddr_in servAddr;
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(80);
    servAddr.sin_addr.S_un.S_addr=inet_addr(lpbuffer);


    ClientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if ( ClientSocket == INVALID_SOCKET )
    {
        cout<<"Create Socket Failed::"<<GetLastError()<<endl;
        return -1;
    }

    if(connect(ClientSocket,(struct sockaddr*)&servAddr, sizeof(servAddr))== -1)
    {
        cout << "error" <<endl;
        exit(1);
    }
    else cout <<"success connected" << endl;

    if(send(ClientSocket, request, (int)strlen(request), 0) == -1)
    {
        cout << "send error" << endl;
        exit(1);
    }
    else cout << "sended success!" << endl;

    char buffer[10000];
    int nbytes;
    if((nbytes=recv(ClientSocket,buffer,1024,0)) == -1)
    {
        cout << "read error" << endl;
        exit(1);
    }
    else cout << "read success";
    cout << "\n--------------------------"<<endl;
    cout << nbytes << endl;
    cout << buffer << endl;
    return 0;
}

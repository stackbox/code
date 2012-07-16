// sockhttp1Dlg.cpp : implementation file
//

#include "stdafx.h"
#include "sockhttp1.h"
#include "sockhttp1Dlg.h"
#include <winsock2.h>
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
#pragma comment(lib,"ws2_32.lib")
/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CSockhttp1Dlg dialog

CSockhttp1Dlg::CSockhttp1Dlg(CWnd* pParent /*=NULL*/)
	: CDialog(CSockhttp1Dlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CSockhttp1Dlg)
	m_addr = _T("");
	m_request = _T("");
	m_responce = _T("");
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CSockhttp1Dlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CSockhttp1Dlg)
	DDX_Text(pDX, IDC_EDIT_ADDR, m_addr);
	DDX_Text(pDX, IDC_REQUEST, m_request);
	DDX_Text(pDX, IDC_RESPONSE, m_responce);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CSockhttp1Dlg, CDialog)
	//{{AFX_MSG_MAP(CSockhttp1Dlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CSockhttp1Dlg message handlers

BOOL CSockhttp1Dlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	
	// TODO: Add extra initialization here
	
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CSockhttp1Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CSockhttp1Dlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CSockhttp1Dlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CSockhttp1Dlg::OnOK() 
{
	// TODO: Add extra validation here

	WSADATA Ws;
    SOCKET ClientSocket;
	char request[1024] = "GET /index.html HTTP/1.1\r\nHost:";
	char *re_end=" Connection: Keep-Alive\r\n\r\n";

	if (WSAStartup(MAKEWORD(2,2), &Ws) != 0 )
    {
        exit(1);
    }
	UpdateData(TRUE);
	CString addr = m_addr;
	LPTSTR p = addr.GetBuffer(addr.GetLength());
    
	strcat(request,p);
	strcat(request,re_end);

	HOSTENT *host_entry = gethostbyname(p);
	LPTSTR lpbuffer = inet_ntoa(*((struct in_addr *)host_entry->h_addr)) ;
	::AfxMessageBox(lpbuffer);

	sockaddr_in servAddr;
    servAddr.sin_family = AF_INET;
    servAddr.sin_port = htons(80);
    servAddr.sin_addr.S_un.S_addr=inet_addr(lpbuffer);
	ClientSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if ( ClientSocket == INVALID_SOCKET )
    {
       exit(-1);
    }
	if(connect(ClientSocket,(struct sockaddr*)&servAddr, sizeof(servAddr))== -1)
    {
        exit(-1);
    }
	if(send(ClientSocket, request, (int)strlen(request), 0) == -1)
    {
        exit(-1);
    } 
	char buffer[4048];
    int nbytes;
    if((nbytes=recv(ClientSocket,buffer,4048,0)) == -1)
    {
        exit(-1);
    }
	buffer[nbytes] = '\0';

	CString str_responce;
	str_responce.Format(buffer);
	m_responce = str_responce;
    CString str_request;
	str_request.Format(request);
    m_request = str_request;
    UpdateData(FALSE);
	//CDialog::OnOK();
}

void CSockhttp1Dlg::OnCancel() 
{
		CDialog::OnCancel();
}

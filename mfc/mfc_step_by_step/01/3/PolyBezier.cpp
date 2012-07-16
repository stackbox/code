#include <afxwin.h>
#include "PolyBezier.h"

CMyApp myApp;

BOOL CMyApp::InitInstance()
{
	m_pMainWnd = new CMainWindow;
	m_pMainWnd->ShowWindow(m_nCmdShow);
	m_pMainWnd->UpdateWindow();
	return true;
}

BEGIN_MESSAGE_MAP(CMainWindow,CFrameWnd)
	ON_WM_PAINT()
END_MESSAGE_MAP()

CMainWindow::CMainWindow()
{
	Create(NULL,_T("A PolyBezier Application"));
}

void CMainWindow::OnPaint()
{
	CPaintDC dc(this);
	POINT point1[] = {120,100,120,200,250,150,500,40};
	POINT point2[] = {120,100,50,350,250,200,500,40};

	dc.PolyBezier(point1,4);
	dc.PolyBezier(point2,4);
}
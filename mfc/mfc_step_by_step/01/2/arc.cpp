#include <afxwin.h>
#include "arc.h"

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
	Create(NULL, _T("A arc application"));
}

void CMainWindow::OnPaint()
{
	CPaintDC dc(this);
	
	CRect rect1(0,0,200,100);
	CPoint point1(0,50);
	CPoint point2(100,0);
	dc.MoveTo(0,50);
	dc.Arc(rect1,point1,point2);
	dc.LineTo(100,50);
    //Arc不改变画笔位置

	dc.MoveTo(0,200);
	CRect rect2(0,150,200,250);
	CPoint point3(0,200);
	CPoint point4(100,150);
	dc.ArcTo(rect2,point3,point4);
	dc.LineTo(100,200);
	//ArcTo改变画笔位置

}

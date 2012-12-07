// sockhttp1Dlg.h : header file
//

#if !defined(AFX_SOCKHTTP1DLG_H__3E9ECAD4_7893_4FF6_A541_FA462B2226D1__INCLUDED_)
#define AFX_SOCKHTTP1DLG_H__3E9ECAD4_7893_4FF6_A541_FA462B2226D1__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CSockhttp1Dlg dialog

class CSockhttp1Dlg : public CDialog
{
// Construction
public:
	CSockhttp1Dlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CSockhttp1Dlg)
	enum { IDD = IDD_SOCKHTTP1_DIALOG };
	CString	m_addr;
	CString	m_request;
	CString	m_responce;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSockhttp1Dlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CSockhttp1Dlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	virtual void OnOK();
	virtual void OnCancel();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SOCKHTTP1DLG_H__3E9ECAD4_7893_4FF6_A541_FA462B2226D1__INCLUDED_)

// sockhttp1.h : main header file for the SOCKHTTP1 application
//

#if !defined(AFX_SOCKHTTP1_H__9F046408_6B3A_401C_97D3_3AD5A0A0CB6D__INCLUDED_)
#define AFX_SOCKHTTP1_H__9F046408_6B3A_401C_97D3_3AD5A0A0CB6D__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CSockhttp1App:
// See sockhttp1.cpp for the implementation of this class
//

class CSockhttp1App : public CWinApp
{
public:
	CSockhttp1App();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSockhttp1App)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CSockhttp1App)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SOCKHTTP1_H__9F046408_6B3A_401C_97D3_3AD5A0A0CB6D__INCLUDED_)

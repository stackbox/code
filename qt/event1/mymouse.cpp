#include "mymouse.h"

MouseEvent::MouseEvent() : QMainWindow()
{
	setWindowTitle(tr("Get Mouse Event"));
	labelStatus = new QLabel();
	labelStatus->setText(tr("Mouse Position:"));
	labelStatus->setFixedWidth(100);
	labelMousePos = new QLabel();
	labelMousePos->setText(tr(""));
	labelMousePos->setFixedWidth(100);

	statusBar()->addPermanentWidget(labelStatus);
	statusBar()->addPermanentWidget(labelMousePos);
	this->setMouseTracking(true);
}

void MouseEvent::mousePressEvent(QMouseEvent *e)
{
	QString str = "(" + QString::number(e->x()) + "," + QString::number(e->y())+")";
	if(e->button() == Qt::LeftButton)
	{
		statusBar()->showMessage(tr("Mouse Left Button Pressed:")+str);
	} else if(e->button() ==  Qt::RightButton)
	{
		statusBar()->showMessage(tr("Mouse Right Button Pressed:")+str);
	} else if(e->button() == Qt::MidButton)
	{
		statusBar()->showMessage(tr("Mouse Mid Button Pressed:")+str);
	}
}


void MouseEvent::mouseMoveEvent(QMouseEvent *e)
{
	labelMousePos->setText("("+QString::number(e->x())+","+QString::number(e->y())+")");
}

void MouseEvent::mouseReleaseEvent(QMouseEvent *e)
{
	QString str="("+QString::number(e->x())+","+QString::number(e->y())+")";
	statusBar()->showMessage(tr("Mouse Released:")+str,3000);
}

void MouseEvent::mouseDoubleClickEvent(QMouseEvent *e)
{
	QString str="("+QString::number(e->x())+","+QString::number(e->y())+")";
	if(e->button() == Qt::LeftButton)
	{
		statusBar()->showMessage(tr("Mouse Left double clicked:")+str);
	} else if(e->button() == Qt::RightButton)
	{
    	statusBar()->showMessage(tr("Mouse Right double clicked:")+str);
	} else if(e->button() == Qt::MidButton)
	{
    	statusBar()->showMessage(tr("Mouse Mid double clicked:")+str);
	}
}





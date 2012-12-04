#include <QApplication>
#include <QtGui>
#include <QMainWindow>
#include <QLabel>
#include <QMouseEvent>

class MouseEvent : public QMainWindow
{
	Q_OBJECT
public:
		MouseEvent();
private:
		QLabel *labelStatus;
		QLabel *labelMousePos;
protected:
		void mouseMoveEvent(QMouseEvent * e);
		void mousePressEvent(QMouseEvent * e);
		void mouseReleaseEvent(QMouseEvent * e);
		void mouseDoubleClickEvent(QMouseEvent * e);
};


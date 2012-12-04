#include <QApplication>
#include <QtDialog>
#include <QThread>
#include <QString>
#include <QCloseEvent>
#include <QPushButton>

class Thread : public QThread
{
	Q_OBJECT
public:
		Thread();
		void setMessage(const QString &message);
		void stop();
protected:
		void run();
private:
		QString messageStr;
		volatile bool stopped;
};

class ThreadDialog : public QDialog
{
	Q_OBJECT
public:
		ThreadDialog(QWidget *parent = 0);
protected:
		void closeEvent(QCloseEvent *event);
private slots:
		void startOrStopThreadA();
		void startOrStopThreadB();
private:
		Thread threadA;
		Thread threadB;
		QPushButton *threadAButton;
		QPushButton *threadBButton;
		QPushButton *quitButton;
};
		


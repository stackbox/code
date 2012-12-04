#include "threads.h"

Thread::Thread()
{
	stopped = false;
}

void Thread::run()
{
	while(!stopped)
		cerr << qPrintable(messageStr);
	stopped = false;
	cerr << endl;
}

void Thread::stop()
{
	stopped = true;
}

ThreadDialog::ThreadDialog(QWidget *parent)
	:  QDialog(parent)
{
	threadA.setMessage("A");
	threadB.setMessage("B");
	threadAButton = new QPushButton(tr("Start A"));
	threadBButton = new QPushButton(tr("Start B"));
	quitButton = new QPushButton(tr("Quit"));
	quitButton->setDefault(true);

	connect(threadAButton,SIGNAL(clicked()),
			this,SLOT(startOrStopThreadA()));
	connect(threadBButton,SIGNAL(clicked()),
			this,SLOT(startOrStopThreadB()));
}


void ThreadDialog::startOrStopThreadA()
{
	if(threadA.isRunning()) {
		threadA.stop();
		threadAButton->setText(tr("Start A"));
	} else {
		threadA.start();
		threadAButton->setText(tr("Stop A"));
	}
}

void ThreadDialog::startOrStopThreadB()
{
	if(threadB.isRunning()) {
		threadB.stop();
		threadBButton->setText(tr("Start B"));
	} else {
		threadB.start();
		threadBButton->setText(tr("Stop B"));
	}
}


void ThreadDialog::closeEvent(QCloseEvent *event)
{
	threadA.stop();
	threadB.stop();
	threadA.wait();
	threadB.wait();
	event->accept();
}

#include "mymouse.h"

int main(int argc, char **argv)
{
	QApplication app(argc, argv);
	MouseEvent ev;
	ev.show();
	return app.exec();
}


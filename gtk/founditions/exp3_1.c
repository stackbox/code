#include <gtk/gtk.h>

static void destroy(GtkWidget *,gpointer);

int main(int argc, char *argv[])
{

	gtk_init(&argc,&argv);







	return 0;
}

static void destroy(GtkWidget *window,gpointer data)
{
	gtk_main_quit();
}

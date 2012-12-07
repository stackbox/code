/********************************************************************************
** Form generated from reading UI file 'widget.ui'
**
** Created: Mon Nov 19 17:57:16 2012
**      by: Qt User Interface Compiler version 4.8.0
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_WIDGET_H
#define UI_WIDGET_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QComboBox>
#include <QtGui/QGridLayout>
#include <QtGui/QGroupBox>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QPushButton>
#include <QtGui/QTableWidget>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_Widget
{
public:
    QLabel *label;
    QLabel *label_2;
    QLabel *label_3;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QWidget *layoutWidget;
    QGridLayout *gridLayout;
    QLabel *label_8;
    QComboBox *comboBox;
    QTableWidget *tableWidget;
    QGroupBox *groupBox;
    QWidget *layoutWidget1;
    QGridLayout *gridLayout_2;
    QLabel *label_9;
    QLineEdit *lineEdit;
    QLabel *label_10;
    QLineEdit *lineEdit_2;
    QLabel *label_11;
    QLineEdit *lineEdit_3;
    QLabel *label_12;
    QLineEdit *lineEdit_4;
    QLabel *label_13;
    QLineEdit *lineEdit_5;
    QLabel *label_14;
    QLineEdit *lineEdit_6;
    QTableWidget *tableWidget_2;
    QWidget *widget;
    QGridLayout *gridLayout_3;
    QPushButton *pushButton_2;
    QPushButton *pushButton_6;
    QPushButton *pushButton_3;
    QPushButton *pushButton_4;
    QPushButton *pushButton_5;
    QPushButton *pushButton;
    QWidget *widget1;
    QGridLayout *gridLayout_4;
    QLabel *label_16;
    QComboBox *comboBox_2;
    QLabel *label_15;
    QComboBox *comboBox_3;

    void setupUi(QWidget *Widget)
    {
        if (Widget->objectName().isEmpty())
            Widget->setObjectName(QString::fromUtf8("Widget"));
        Widget->resize(685, 518);
        Widget->setMinimumSize(QSize(685, 518));
        Widget->setMaximumSize(QSize(685, 518));
        label = new QLabel(Widget);
        label->setObjectName(QString::fromUtf8("label"));
        label->setGeometry(QRect(350, 20, 301, 211));
        label->setTextFormat(Qt::PlainText);
        label->setPixmap(QPixmap(QString::fromUtf8(":/new/prefix1/RouterGra.gif")));
        label->setScaledContents(false);
        label->setAlignment(Qt::AlignCenter);
        label_2 = new QLabel(Widget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(340, 40, 21, 16));
        label_3 = new QLabel(Widget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(630, 40, 21, 16));
        label_4 = new QLabel(Widget);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(340, 110, 16, 16));
        label_5 = new QLabel(Widget);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(630, 110, 16, 16));
        label_6 = new QLabel(Widget);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(340, 190, 21, 21));
        label_7 = new QLabel(Widget);
        label_7->setObjectName(QString::fromUtf8("label_7"));
        label_7->setGeometry(QRect(630, 190, 21, 21));
        layoutWidget = new QWidget(Widget);
        layoutWidget->setObjectName(QString::fromUtf8("layoutWidget"));
        layoutWidget->setGeometry(QRect(10, 10, 301, 241));
        gridLayout = new QGridLayout(layoutWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QString::fromUtf8("gridLayout"));
        gridLayout->setContentsMargins(0, 0, 0, 0);
        label_8 = new QLabel(layoutWidget);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        QSizePolicy sizePolicy(QSizePolicy::Fixed, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(0);
        sizePolicy.setVerticalStretch(0);
        sizePolicy.setHeightForWidth(label_8->sizePolicy().hasHeightForWidth());
        label_8->setSizePolicy(sizePolicy);
        QFont font;
        font.setFamily(QString::fromUtf8("Arial"));
        font.setBold(true);
        font.setWeight(75);
        label_8->setFont(font);

        gridLayout->addWidget(label_8, 0, 0, 1, 1);

        comboBox = new QComboBox(layoutWidget);
        comboBox->setObjectName(QString::fromUtf8("comboBox"));

        gridLayout->addWidget(comboBox, 0, 1, 1, 1);

        tableWidget = new QTableWidget(layoutWidget);
        if (tableWidget->columnCount() < 3)
            tableWidget->setColumnCount(3);
        QFont font1;
        font1.setKerning(false);
        QTableWidgetItem *__qtablewidgetitem = new QTableWidgetItem();
        __qtablewidgetitem->setText(QString::fromUtf8("\347\233\256\346\240\207"));
        __qtablewidgetitem->setTextAlignment(Qt::AlignHCenter|Qt::AlignVCenter|Qt::AlignCenter);
        __qtablewidgetitem->setFont(font1);
        tableWidget->setHorizontalHeaderItem(0, __qtablewidgetitem);
        QTableWidgetItem *__qtablewidgetitem1 = new QTableWidgetItem();
        tableWidget->setHorizontalHeaderItem(1, __qtablewidgetitem1);
        QTableWidgetItem *__qtablewidgetitem2 = new QTableWidgetItem();
        tableWidget->setHorizontalHeaderItem(2, __qtablewidgetitem2);
        tableWidget->setObjectName(QString::fromUtf8("tableWidget"));
        tableWidget->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
        tableWidget->horizontalHeader()->setDefaultSectionSize(100);

        gridLayout->addWidget(tableWidget, 5, 0, 1, 2);

        groupBox = new QGroupBox(Widget);
        groupBox->setObjectName(QString::fromUtf8("groupBox"));
        groupBox->setGeometry(QRect(10, 270, 301, 231));
        groupBox->setFont(font);
        layoutWidget1 = new QWidget(groupBox);
        layoutWidget1->setObjectName(QString::fromUtf8("layoutWidget1"));
        layoutWidget1->setGeometry(QRect(10, 20, 281, 201));
        gridLayout_2 = new QGridLayout(layoutWidget1);
        gridLayout_2->setSpacing(6);
        gridLayout_2->setContentsMargins(11, 11, 11, 11);
        gridLayout_2->setObjectName(QString::fromUtf8("gridLayout_2"));
        gridLayout_2->setContentsMargins(0, 0, 0, 0);
        label_9 = new QLabel(layoutWidget1);
        label_9->setObjectName(QString::fromUtf8("label_9"));
        sizePolicy.setHeightForWidth(label_9->sizePolicy().hasHeightForWidth());
        label_9->setSizePolicy(sizePolicy);
        QFont font2;
        font2.setBold(false);
        font2.setWeight(50);
        label_9->setFont(font2);

        gridLayout_2->addWidget(label_9, 0, 0, 1, 1);

        lineEdit = new QLineEdit(layoutWidget1);
        lineEdit->setObjectName(QString::fromUtf8("lineEdit"));

        gridLayout_2->addWidget(lineEdit, 0, 1, 1, 1);

        label_10 = new QLabel(layoutWidget1);
        label_10->setObjectName(QString::fromUtf8("label_10"));
        sizePolicy.setHeightForWidth(label_10->sizePolicy().hasHeightForWidth());
        label_10->setSizePolicy(sizePolicy);
        label_10->setFont(font2);

        gridLayout_2->addWidget(label_10, 1, 0, 1, 1);

        lineEdit_2 = new QLineEdit(layoutWidget1);
        lineEdit_2->setObjectName(QString::fromUtf8("lineEdit_2"));

        gridLayout_2->addWidget(lineEdit_2, 1, 1, 1, 1);

        label_11 = new QLabel(layoutWidget1);
        label_11->setObjectName(QString::fromUtf8("label_11"));
        sizePolicy.setHeightForWidth(label_11->sizePolicy().hasHeightForWidth());
        label_11->setSizePolicy(sizePolicy);
        label_11->setFont(font2);

        gridLayout_2->addWidget(label_11, 2, 0, 1, 1);

        lineEdit_3 = new QLineEdit(layoutWidget1);
        lineEdit_3->setObjectName(QString::fromUtf8("lineEdit_3"));

        gridLayout_2->addWidget(lineEdit_3, 2, 1, 1, 1);

        label_12 = new QLabel(layoutWidget1);
        label_12->setObjectName(QString::fromUtf8("label_12"));
        sizePolicy.setHeightForWidth(label_12->sizePolicy().hasHeightForWidth());
        label_12->setSizePolicy(sizePolicy);
        label_12->setFont(font2);

        gridLayout_2->addWidget(label_12, 3, 0, 1, 1);

        lineEdit_4 = new QLineEdit(layoutWidget1);
        lineEdit_4->setObjectName(QString::fromUtf8("lineEdit_4"));

        gridLayout_2->addWidget(lineEdit_4, 3, 1, 1, 1);

        label_13 = new QLabel(layoutWidget1);
        label_13->setObjectName(QString::fromUtf8("label_13"));
        sizePolicy.setHeightForWidth(label_13->sizePolicy().hasHeightForWidth());
        label_13->setSizePolicy(sizePolicy);
        label_13->setFont(font2);

        gridLayout_2->addWidget(label_13, 4, 0, 1, 1);

        lineEdit_5 = new QLineEdit(layoutWidget1);
        lineEdit_5->setObjectName(QString::fromUtf8("lineEdit_5"));

        gridLayout_2->addWidget(lineEdit_5, 4, 1, 1, 1);

        label_14 = new QLabel(layoutWidget1);
        label_14->setObjectName(QString::fromUtf8("label_14"));
        sizePolicy.setHeightForWidth(label_14->sizePolicy().hasHeightForWidth());
        label_14->setSizePolicy(sizePolicy);
        label_14->setFont(font2);

        gridLayout_2->addWidget(label_14, 5, 0, 1, 1);

        lineEdit_6 = new QLineEdit(layoutWidget1);
        lineEdit_6->setObjectName(QString::fromUtf8("lineEdit_6"));

        gridLayout_2->addWidget(lineEdit_6, 5, 1, 1, 1);

        tableWidget_2 = new QTableWidget(Widget);
        if (tableWidget_2->columnCount() < 2)
            tableWidget_2->setColumnCount(2);
        QTableWidgetItem *__qtablewidgetitem3 = new QTableWidgetItem();
        tableWidget_2->setHorizontalHeaderItem(0, __qtablewidgetitem3);
        QTableWidgetItem *__qtablewidgetitem4 = new QTableWidgetItem();
        tableWidget_2->setHorizontalHeaderItem(1, __qtablewidgetitem4);
        tableWidget_2->setObjectName(QString::fromUtf8("tableWidget_2"));
        tableWidget_2->setGeometry(QRect(340, 320, 301, 111));
        widget = new QWidget(Widget);
        widget->setObjectName(QString::fromUtf8("widget"));
        widget->setGeometry(QRect(340, 440, 301, 51));
        gridLayout_3 = new QGridLayout(widget);
        gridLayout_3->setSpacing(6);
        gridLayout_3->setContentsMargins(11, 11, 11, 11);
        gridLayout_3->setObjectName(QString::fromUtf8("gridLayout_3"));
        gridLayout_3->setContentsMargins(0, 0, 0, 0);
        pushButton_2 = new QPushButton(widget);
        pushButton_2->setObjectName(QString::fromUtf8("pushButton_2"));

        gridLayout_3->addWidget(pushButton_2, 0, 0, 1, 1);

        pushButton_6 = new QPushButton(widget);
        pushButton_6->setObjectName(QString::fromUtf8("pushButton_6"));

        gridLayout_3->addWidget(pushButton_6, 0, 1, 1, 1);

        pushButton_3 = new QPushButton(widget);
        pushButton_3->setObjectName(QString::fromUtf8("pushButton_3"));

        gridLayout_3->addWidget(pushButton_3, 0, 2, 1, 1);

        pushButton_4 = new QPushButton(widget);
        pushButton_4->setObjectName(QString::fromUtf8("pushButton_4"));

        gridLayout_3->addWidget(pushButton_4, 1, 0, 1, 1);

        pushButton_5 = new QPushButton(widget);
        pushButton_5->setObjectName(QString::fromUtf8("pushButton_5"));

        gridLayout_3->addWidget(pushButton_5, 1, 1, 1, 1);

        pushButton = new QPushButton(widget);
        pushButton->setObjectName(QString::fromUtf8("pushButton"));

        gridLayout_3->addWidget(pushButton, 1, 2, 1, 1);

        widget1 = new QWidget(Widget);
        widget1->setObjectName(QString::fromUtf8("widget1"));
        widget1->setGeometry(QRect(340, 270, 301, 51));
        gridLayout_4 = new QGridLayout(widget1);
        gridLayout_4->setSpacing(6);
        gridLayout_4->setContentsMargins(11, 11, 11, 11);
        gridLayout_4->setObjectName(QString::fromUtf8("gridLayout_4"));
        gridLayout_4->setContentsMargins(0, 0, 0, 0);
        label_16 = new QLabel(widget1);
        label_16->setObjectName(QString::fromUtf8("label_16"));
        label_16->setAlignment(Qt::AlignCenter);

        gridLayout_4->addWidget(label_16, 0, 0, 1, 1);

        comboBox_2 = new QComboBox(widget1);
        comboBox_2->setObjectName(QString::fromUtf8("comboBox_2"));

        gridLayout_4->addWidget(comboBox_2, 0, 1, 1, 1);

        label_15 = new QLabel(widget1);
        label_15->setObjectName(QString::fromUtf8("label_15"));
        sizePolicy.setHeightForWidth(label_15->sizePolicy().hasHeightForWidth());
        label_15->setSizePolicy(sizePolicy);
        label_15->setAlignment(Qt::AlignCenter);

        gridLayout_4->addWidget(label_15, 1, 0, 1, 1);

        comboBox_3 = new QComboBox(widget1);
        comboBox_3->setObjectName(QString::fromUtf8("comboBox_3"));

        gridLayout_4->addWidget(comboBox_3, 1, 1, 1, 1);

        layoutWidget->raise();
        label->raise();
        label_2->raise();
        label_3->raise();
        label_4->raise();
        label_5->raise();
        label_6->raise();
        label_7->raise();
        groupBox->raise();
        pushButton->raise();
        pushButton_2->raise();
        pushButton_3->raise();
        pushButton_4->raise();
        pushButton_5->raise();
        pushButton_6->raise();
        label_15->raise();
        label_16->raise();
        comboBox_2->raise();
        comboBox_3->raise();
        tableWidget_2->raise();

        retranslateUi(Widget);

        QMetaObject::connectSlotsByName(Widget);
    } // setupUi

    void retranslateUi(QWidget *Widget)
    {
        Widget->setWindowTitle(QApplication::translate("Widget", "\345\237\272\344\272\216\346\265\201\351\207\217\345\210\206\346\236\220\347\232\204\350\267\257\347\224\261\347\256\227\346\263\225\346\250\241\346\213\237", 0, QApplication::UnicodeUTF8));
        label->setText(QString());
        label_2->setText(QApplication::translate("Widget", "R0", 0, QApplication::UnicodeUTF8));
        label_3->setText(QApplication::translate("Widget", "R1", 0, QApplication::UnicodeUTF8));
        label_4->setText(QApplication::translate("Widget", "R2", 0, QApplication::UnicodeUTF8));
        label_5->setText(QApplication::translate("Widget", "R3", 0, QApplication::UnicodeUTF8));
        label_6->setText(QApplication::translate("Widget", "R4", 0, QApplication::UnicodeUTF8));
        label_7->setText(QApplication::translate("Widget", "R5", 0, QApplication::UnicodeUTF8));
        label_8->setText(QApplication::translate("Widget", "ROUTER: ", 0, QApplication::UnicodeUTF8));
        comboBox->clear();
        comboBox->insertItems(0, QStringList()
         << QApplication::translate("Widget", "Router0", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Widget", "Router1", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Widget", "Router2", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Widget", "Router3", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Widget", "Router4", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("Widget", "Router5", 0, QApplication::UnicodeUTF8)
        );
        QTableWidgetItem *___qtablewidgetitem = tableWidget->horizontalHeaderItem(1);
        ___qtablewidgetitem->setText(QApplication::translate("Widget", "\345\207\272\345\217\243", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem1 = tableWidget->horizontalHeaderItem(2);
        ___qtablewidgetitem1->setText(QApplication::translate("Widget", "Metric", 0, QApplication::UnicodeUTF8));
        groupBox->setTitle(QApplication::translate("Widget", "\350\267\257\347\224\261\346\265\201\351\207\217\357\274\2101~100\357\274\211", 0, QApplication::UnicodeUTF8));
        label_9->setText(QApplication::translate("Widget", "Router0:", 0, QApplication::UnicodeUTF8));
        label_10->setText(QApplication::translate("Widget", "Router1:", 0, QApplication::UnicodeUTF8));
        label_11->setText(QApplication::translate("Widget", "Router2:", 0, QApplication::UnicodeUTF8));
        label_12->setText(QApplication::translate("Widget", "Router3:", 0, QApplication::UnicodeUTF8));
        label_13->setText(QApplication::translate("Widget", "Router4:", 0, QApplication::UnicodeUTF8));
        label_14->setText(QApplication::translate("Widget", "Router5:", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem2 = tableWidget_2->horizontalHeaderItem(0);
        ___qtablewidgetitem2->setText(QApplication::translate("Widget", "\347\274\226\345\217\267", 0, QApplication::UnicodeUTF8));
        QTableWidgetItem *___qtablewidgetitem3 = tableWidget_2->horizontalHeaderItem(1);
        ___qtablewidgetitem3->setText(QApplication::translate("Widget", "\347\273\217\350\277\207\350\267\257\347\224\261", 0, QApplication::UnicodeUTF8));
        pushButton_2->setText(QApplication::translate("Widget", "\345\274\200\345\247\213\350\256\241\347\256\227", 0, QApplication::UnicodeUTF8));
        pushButton_6->setText(QApplication::translate("Widget", "\351\207\215\347\275\256", 0, QApplication::UnicodeUTF8));
        pushButton_3->setText(QApplication::translate("Widget", "\346\237\245\347\234\213\350\267\257\345\276\204", 0, QApplication::UnicodeUTF8));
        pushButton_4->setText(QApplication::translate("Widget", "\345\210\235\345\247\213\345\214\226", 0, QApplication::UnicodeUTF8));
        pushButton_5->setText(QApplication::translate("Widget", "\345\205\263\344\272\216", 0, QApplication::UnicodeUTF8));
        pushButton->setText(QApplication::translate("Widget", "\351\200\200\345\207\272", 0, QApplication::UnicodeUTF8));
        label_16->setText(QApplication::translate("Widget", "\350\265\267\345\247\213\350\267\257\347\224\261\357\274\232", 0, QApplication::UnicodeUTF8));
        label_15->setText(QApplication::translate("Widget", "\347\233\256\347\232\204\350\267\257\347\224\261\357\274\232", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class Widget: public Ui_Widget {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_WIDGET_H

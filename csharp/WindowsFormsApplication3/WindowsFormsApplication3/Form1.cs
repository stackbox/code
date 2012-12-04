using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace WindowsFormsApplication3
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            if (checkBox1.BackColor == System.Drawing.Color.Red)
                checkBox1.BackColor = System.Drawing.Color.LightGray;
            else
                checkBox1.BackColor = System.Drawing.Color.Red;
        }

        private void textBox1_DoubleClick(object sender, EventArgs e)
        {
            textBox1.ForeColor = System.Drawing.Color.White;
            textBox1.BackColor = System.Drawing.Color.Black;
        }

        
       

        

      
       
    }
}

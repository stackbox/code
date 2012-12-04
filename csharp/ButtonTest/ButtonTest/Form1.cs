using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace ButtonTest
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            this.btnOK.Enabled = false;

            this.txtAddress.Tag = false;
            this.txtAge.Tag = false;
            this.txtName.Tag = false;
            this.txtOccupation.Tag = false;

            this.txtName.Validating += new 
        }

        private void btnOK_Click(object sender, EventArgs e)
        {
            string output;

            output = "Name:" + this.txtName.Text + "\r\n";
            output += "Address:" + this.txtAddress.Text + "\r\n";
            output += "Occupation:" + this.txtOccupation.Text + "\r\n";
            output += "Age:" + this.txtAge.Text;

            this.txtOutput.Text = output;
        }

        private void btnHelp_Click(object sender, EventArgs e)
        {
            string output;

            output = "Name = Your name\r\n";
            output += "Address = Your address\r\n";
            output += "Occupation = Only allowed value is 'programer'\r\n";
            output += "Age = Your age";

            this.txtOutput.Text = output;
        }

        

       
    }
}

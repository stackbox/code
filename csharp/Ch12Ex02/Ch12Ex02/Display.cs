using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ch12Ex02
{
    public class Display
    {
        public void DisplayMessage(Connection source,MessageArrivedEventArgs e)
       {
           Console.WriteLine("message arrived form {0}", source.Name);
           Console.WriteLine("message text: {0}", e.Message);
       }
    }
}

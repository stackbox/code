using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Ch09ClassLib;

namespace ConsoleApplication3
{
    class Program
    {
        static void Main(string[] args)
        {
            MyExternalClass obj = new MyExternalClass();
            Console.WriteLine(obj.ToString());
        }
    }
}

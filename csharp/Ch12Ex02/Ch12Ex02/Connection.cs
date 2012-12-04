using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Timers;

namespace Ch12Ex02
{
    public delegate void MessageHandler(Connection source,MessageArrivedEventArgs e);

    public class Connection
    {
        public event MessageHandler MessageArrived;

        private Timer pollTimer;
        private string name;

        public string Name
        {
            get
            {
                return name;
            }
            set
            {
                name = value;
            }
        }

        public Connection()
        {
            pollTimer = new Timer();
            pollTimer.Elapsed += new ElapsedEventHandler(CheckForMessage);
        }

        public void Connect()
        {
            pollTimer.Start();
        }

        public void Disconnect()
        {
            pollTimer.Stop();
        }

        private void CheckForMessage(object source, ElapsedEventArgs e)
        {
            Console.WriteLine("checking for new messages.");
            Random random = new Random();
            if ((random.Next(9) == 1) && (MessageArrived != null))
            {
                MessageArrived(this, new MessageArrivedEventArgs("hello mum!\n"));
            }
        }

    }
}

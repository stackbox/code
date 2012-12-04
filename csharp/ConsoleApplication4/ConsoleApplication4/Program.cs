using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Ch10CardLib;

namespace ConsoleApplication4
{
    class Program
    {
        static void Main(string[] args)
        {
            Deck myDeck = new Deck();
            myDeck.Shuffle();

            for (int i = 0; i < 52; i++)
            {
                Card tempCard = myDeck.GetCard(i);
                Console.WriteLine(i.ToString()+" : "+tempCard.ToString());

            }
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ch12CardLib
{
    public class Deck:ICloneable
    {
        private Cards cards = new Cards();

        public object Clone()
        {
            Deck newDeck = new Deck((Cards)cards.Clone());
            return newDeck;
        }

        private Deck(Cards newCards)
        {
            cards = newCards;
        }

        public Deck()
        {
            
            for (int suitVal = 0; suitVal < 4; suitVal++)
            {
                for (int rankVal = 1; rankVal < 14; rankVal++)
                {
                    cards.Add(new Card((Suit)suitVal,(Rank)rankVal));
                }
            }
        }

      

        public Deck(bool isAceHigh)
            : this()
        {
            Card.isAceHigh = isAceHigh;
        }

        public Deck(bool useTrumps, Suit trump)
            : this()
        {
            Card.useTrumps = useTrumps;
            Card.trump = trump;
        }

        public Deck(bool isAceHigh, bool useTrumps, Suit Trump)
            : this()
        {
            Card.isAceHigh = isAceHigh;
            Card.useTrumps = useTrumps;
            Card.trump = Trump;
        }

        public Card GetCard(int cardNum)
        {
            if (cardNum >= 0 && cardNum <= 51)
                return cards[cardNum];
            else
                throw (new CardOutOfRangeException((Cards)cards.Clone()));
        }

        public void Shuffle()
        {
            Cards newDeck = new Cards();
            bool[] assigned = new bool[52];

            for (int i = 0; i < 52; i++)
            {
                int sourceCard = 0;
                bool foundCard = false;
                Random sourceGen = new Random();

                while (foundCard == false)
                {
                    sourceCard = sourceGen.Next(52);
                    if (assigned[sourceCard] == false)
                        foundCard = true;
                }
                assigned[sourceCard] = true;
                newDeck.Add(cards[sourceCard]);
            }
            cards = newDeck;
        }

    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ch10CardLib
{
    public enum Suit
    {
        Club,
        Diamond,
        Heart,
        Spade
    }

    public enum Rank
    {
        Ace = 1,
        Deuce,
        Three,
        Four,
        Five,
        Six,
        Seven,
        Eight,
        Nine,
        Ten,
        Jake,
        Queen,
        King
    }

    public class Card
    {
        public readonly Suit suit;
        public readonly Rank rank;

        public override string ToString()
        {
            return "The " + rank + " of " + suit + "s";
        }

        private Card()
        {
        }

        public Card(Suit newSuit, Rank newRank)
        {
            suit = newSuit;
            rank = newRank;
        }
    }
}

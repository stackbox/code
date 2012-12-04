using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ch11CardLib
{
    public class CardOutOfRangeException : Exception
    {
        private Cards deckContents;

        public Cards DeckContents
        {
            get
            {
                return deckContents;
            }
        }

        public CardOutOfRangeException(Cards sourceDeckContents) :
            base("there are onlly 52 cards in the deck.")
        {
            deckContents = sourceDeckContents;
        }
    }
}

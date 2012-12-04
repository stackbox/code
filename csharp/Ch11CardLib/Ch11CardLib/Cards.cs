using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;

namespace Ch11CardLib
{
    public class Cards:CollectionBase,ICloneable
    {
        public object Clone()
        {
            Cards newCards = new Cards();
            foreach (Cards sourceCard in List)
            {
                newCards.Add((Card)sourceCard.Clone());
            }
            return newCards;
        }

        public void Add(Card newCard)
        {
            List.Add(newCard);
        }

        public void Remove(Card oldCard)
        {
            List.Remove(oldCard);
        }

        public Cards()
        {
        }

        public Card this[int cardIndex]
        {
            get
            {
                return (Card)List[cardIndex];
            }
            set
            {
                List[cardIndex] = value;
            }
        }

        public bool Contains(Card card)
        {
            return InnerList.Contains(card);
        }
    }
}

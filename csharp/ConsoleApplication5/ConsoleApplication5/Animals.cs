using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;

namespace ConsoleApplication5
{
    public class Animals:CollectionBase
    {
        public void Add(Animals newAnimal)
        {
            List.Add(newAnimal);
        }

        public void Remove(Animals newAnimal)
        {
            List.Remove(newAnimal);
        }

        public Animals()
        {
        }



        public int Property
        {
            get
            {
                throw new System.NotImplementedException();
            }
            set
            {
            }
        }

        public int Property1
        {
            get
            {
                throw new System.NotImplementedException();
            }
            set
            {
            }
        }

    }
}

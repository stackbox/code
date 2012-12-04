using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;

namespace ConsoleApplication6
{
    class Program
    {
        static void Main(string[] args)
        {
            Person[] persons = new Person[4];
            persons[0] = new Person("amy");
            persons[1] = new Person("bruce");
            persons[2] = new Person("cacy");
            persons[3] = new Person("doctor");

            IEnumerator enumerator = persons.GetEnumerator();
            while (enumerator.MoveNext())
            {
                Person p = (Person)enumerator.Current;
                Console.WriteLine(p.ToString());
            }
          
        }
    }

    class Person
    {
        public Person(string s)
        {
            this.name = s;
        }

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
       
        private string name;
    }

}

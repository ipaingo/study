using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Incapsulation.Weights
{
    public class Indexer
    {
        public int Length { get; }
        public double[] Array;
        public int Start { get; }


        public Indexer(double[] array, int start, int length)
        {
            // если входные данные противоречат здравому смыслу, исключение. 
            if (start + length > array.Length || start < 0 || length < 0)
                throw new ArgumentException();
            Length = length;
            Start = start;
            Array = array;
        }

        public double this[int index]
        {
            get
            {
                // исключение на случай выхода за пределы.
                if (index < 0 || index >= Length)
                    throw new IndexOutOfRangeException();
                // возвращаем со смещением Start.
                return Array[Start + index];
            }

            set
            {
                if (index < 0 || index >= Length)
                    throw new IndexOutOfRangeException();
                Array[Start + index] = value;
            }
        }
    }
}

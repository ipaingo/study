using System;
using System.Collections;
using System.Collections.Generic;

namespace hashes
{
	public class ReadonlyBytes
	{
        byte[] hashArr; // массив байтовых чисел.
        public int Length { get; }

        int hash = 0;

        public ReadonlyBytes(params byte[] bytes)
        {
            // тест на исключения при создании просит ArgumentNullException, если в функцию передали нулл.
            if (bytes == null)
            {
                throw new ArgumentNullException("bytes");
            }


            Length = bytes.Length; // просто длина.


            hashArr = new byte[Length]; // сделаем массив из того, что получено на вход.
            for (int i = 0; i < Length; i++)
            {
                hashArr[i] = bytes[i];
            }

            SetHashCode();
        }

        public byte this[int index]
        {
            get
            {
                if (index < 0 || index > Length)
                    throw new IndexOutOfRangeException("index");
                // в тестах (что логично) просят вернуть ошибку выхода за пределы массива
                // при обращении к числу вне границ.
                return hashArr[index];
            }
        }

        public IEnumerator<byte> GetEnumerator()
        {
            foreach (var e in hashArr)
            {
                yield return e;
            }
        }

        // переопределяем Equals для массивов байт.
        public override bool Equals(object otherObject)
        {
            // null не равен массиву байт.
            if (otherObject is null)
                return false;

            // логично, что они не equal, если они не разного типа.
            if (otherObject.GetType() != typeof(ReadonlyBytes))
                return false;

            // для дальнейшего сравнения будем рассматривать another как объект класса.
            var byteObject = otherObject as ReadonlyBytes;
            // совпадение по длине.
            if (byteObject.Length != Length)
                return false;

            // совпадение по значениям.
            for (int i = 0; i < hashArr.Length; i++)
                if (byteObject[i] != hashArr[i])
                    return false;

            // если все совпало, значит, equal.
            return true;
        }

        public override int GetHashCode()
        {
            return hash;
        }

        public void SetHashCode()
        {
            // полиномиальный хэш.
            hash = 0;
            int k = 257; 
            int m = 1;
            unchecked   // ругается на переполнение, а мы делаем вид, что ничего не знаем.
            {           // на самом деле можно избежать, делая модуляцию, но unchecked и сам все усечет.
                foreach (var x in hashArr)
                {
                    hash = hash + m * x;
                    m = m * k;
                }
            }
        }

        // переписываем ToString, как просят в тестах.
        public override string ToString()
        {
            // открывающая скобочка,
            string answer = "[";
            for (int i = 0; i < Length; i++)
            {
                // значение и запятая,
                answer += hashArr[i].ToString();
                answer += ", ";
            }
            // убираем лишнюю последнюю запятую,
            if (answer.Length - 2 > 0)
                answer = answer.Remove(answer.Length - 2);
            // закрывающая скобочка.
            answer += "]";

            return answer;
        }
    }
}
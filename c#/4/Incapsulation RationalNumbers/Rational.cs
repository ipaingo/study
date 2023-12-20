using NUnit.Framework.Constraints;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Incapsulation.RationalNumbers
{

    public struct Rational
    {
        public bool IsNan;
        public int Numerator;
        public int Denominator;

        public Rational(int a = 1, int b = 1)
        {
            if (a == 0 && b != 0)
                b = 1;

            if (b < 0)
            {
                a *= -1;
                b *= -1;
            }

            IsNan = b == 0;

            int gdc = GCD(a, b);
            if (IsNan || a == 0)
            {
                gdc = 1;
            }

            Numerator = a / gdc;
            Denominator = b / gdc;
        }

        static int GCD(int a, int b)
        {
            a = Math.Abs(a);
            b = Math.Abs(b);

            if (a < b)
            {
                (a, b) = (b, a);
            }

            while (b != 0)
            {
                a %= b;
                (a, b) = (b, a);
            }

            return a;
        }

        public static Rational operator +(Rational a, Rational b)
        {
            return new Rational(a.Numerator * b.Denominator + b.Numerator * a.Denominator, a.Denominator * b.Denominator);
        }

        public static Rational operator -(Rational a, Rational b)
        {
            return new Rational(a.Numerator * b.Denominator - b.Numerator * a.Denominator, a.Denominator * b.Denominator);
        }

        public static Rational operator *(Rational a, Rational b)
        {
            return new Rational(a.Numerator * b.Numerator, a.Denominator * b.Denominator);
        }

        public static Rational operator /(Rational a, Rational b)
        {
            return a * new Rational(b.Denominator, b.Numerator * (b.IsNan ? 0 : 1));
        }

        public static implicit operator double(Rational a)
        {
            return a.IsNan ? double.NaN : (double)a.Numerator / (double)a.Denominator;
        }

        public static implicit operator int(Rational a)
        {
            if (a.Denominator != 1)
                throw new Exception();
            return a.Numerator / a.Denominator;
        }

        public static implicit operator Rational(int value)
        {
            return new Rational(value);
        }
    }
}

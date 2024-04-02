using System.Numerics;
using System;
using System.Security.Cryptography;
using System.Runtime.CompilerServices;

// возведение в степень. рекурсия.
BigInteger BinPow(BigInteger n, BigInteger k, BigInteger mod)
{
    if (k == 0)
        return new BigInteger(1);
    if (k == 1)
        return n % mod;

    // деление с остатком.
    var mid = BinPow(n, k / 2, mod);
    return mid * mid * (k % 2 == 1 ? n : 1) % mod;
}

// функция поиска простых чисел с помощью решета Эратосфена.
// используется для предподсчета массива небольших простых чисел.
List<int> generateLowPrimes()
{
    bool[] sieve = new bool[2000];
    for (int i = 2; i < 2000; i++)
        if (!sieve[i])
            for (int j = i * i; j < 2000; j += i)
                sieve[j] = true;

    var primes = new List<int>();
    for (int i = 2; i < 2000; i++)
        if (!sieve[i])
            primes.Add(i);

    return primes;
}

var lowPrimes = generateLowPrimes();

// определяет, является ли число простым. тест Миллера-Рабина.
bool isMaybePrime(BigInteger prime)
{
    for (int i = 0; i < lowPrimes.Count; i++)
    {
        int lp = lowPrimes[i];
        if (lp == prime)
            return true;
        if (prime % lp == 0)
        {
            return false;
        }
    }

    int s = 0;
    BigInteger t = prime - 1;
    while (t % 2 == 0)
    {
        t /= 2;
        s++;
    }

    int iters = 256;
    while (iters-- > 0)
    {
        var a = RandBigIntegerInRange(2, prime - 2);
        var x = BinPow(a, t, prime);
        if (x == 1 || x == prime - 1)
            continue;

        bool flag = true;
        for (int i = 1; i < s; i++)
        {
            x = BinPow(x, 2, prime);
            if (x == 1)
                return false;
            if (x == prime - 1)
            {
                flag = false;
                break;
            }
        }
        if (flag)
        {
            return false;
        }
    }

    return true;
}

// генерирует случайное число в заданном отрезке.
BigInteger RandBigIntegerInRange(BigInteger minValue, BigInteger maxValue)
{
    if (minValue == maxValue) return minValue;

    var random = new Random();
    BigInteger zeroBasedUpperBound = maxValue - 1 - minValue;
    byte[] bytes = zeroBasedUpperBound.ToByteArray();

    byte lastByteMask = 0b11111111;
    for (byte mask = 0b10000000; mask > 0; mask >>= 1, lastByteMask >>= 1)
    {
        if ((bytes[bytes.Length - 1] & mask) == mask) break;
    }

    while (true)
    {
        random.NextBytes(bytes);
        bytes[bytes.Length - 1] &= lastByteMask;
        var result = new BigInteger(bytes);
        if (result <= zeroBasedUpperBound) return result + minValue;
    }
}

// функция генерации случайного простого числа.
BigInteger getRandomPrime()
{
    while (true)
    {
        // по сути генерирует псевдослучайное число и проверяет,
        // не получилось ли оно составным.
        int bits = 256;
        BigInteger min = 1, max = 2;
        while (--bits > 0)
        {
            min *= 2;
            max *= 2;
        }
        min++;
        max--;
        var prime = RandBigIntegerInRange(min, max);
        if (prime % 2 == 0)
            prime += 1;
        if (!isMaybePrime(prime))
            continue;
        return prime;
    }
}

// функция нахождения наибольшего общего делителя.
// используется в китайской теореме об остатках.
BigInteger GCD(BigInteger a, BigInteger b)
{
    if (b > a)
        (a, b) = (b, a);
    while (b > 0)
    {
        a %= b;
        (a, b) = (b, a);
    }

    return a;
}

// функция вычисления закрытого ключа. расширенный алгоритм Евклида.
BigInteger GCDex(BigInteger a, BigInteger b, out BigInteger x, out BigInteger y)
{
    if (a == 0)
    {
        x = 0; y = 1;
        return b;
    }
    BigInteger x1, y1;
    BigInteger d = GCDex(b % a, a, out x1, out y1);
    x = y1 - (b / a) * x1;
    y = x1;
    return d;
}

// функция генерации RSA ключей.
void generateRSAKeys(BigInteger e, out BigInteger d, out BigInteger n, out BigInteger p, out BigInteger q)
{
    BigInteger f;
    do
    {
        // генерирует случайные простые p и q.
        p = getRandomPrime();
        q = getRandomPrime();
        n = p * q;
        f = (p - 1) * (q - 1);
    } while (GCD(e, f) != 1);

    // закрытый ключ d генерируется с помощью расширенного алгоритма Евклида.
    GCDex(e, f, out d, out BigInteger y);
    d = (d % f + f) % f;
}


// получает электронную подпись.
BigInteger getCert(in BigInteger m, in BigInteger d, in BigInteger n, in BigInteger p, in BigInteger q)
{
    // для вычисления используется китайская теорема об остатках.
    var r1 = BinPow(m % p, d % (p - 1), p);
    var r2 = BinPow(m % q, d % (q - 1), q);

    BigInteger m1, m2;
    GCDex(q, p, out m1, out BigInteger y1);
    GCDex(p, q, out m2, out BigInteger y2);
    m1 = (m1 % p + p) % p;
    m2 = (m2 % q + q) % q;

    return (r1 * m1 * q + r2 * m2 * p) % n;
}

// проверка электронной подписи.
bool validateCert(in BigInteger m, in BigInteger cert, in BigInteger e, BigInteger n)
{
    return m == BinPow(cert, e, n);
}


BigInteger m = 1111;
BigInteger e = 1399;
BigInteger n, d, p, q;
generateRSAKeys(e, out d, out n, out p, out q);

Console.WriteLine($"Открытый ключ (n, e): ({n}, {e})");
Console.WriteLine($"Закрытый ключ (n, d): ({n}, {d})");

var cert = getCert(m, d, n, p, q);

Console.WriteLine("Электронная подпись:");
Console.WriteLine(cert);

if (validateCert(m, cert, e, n))
{
    Console.WriteLine("Электронная подпись действительна.");
}
else
{
    Console.WriteLine("Электронная подпись недействительна.");
}

if (validateCert(m, cert + 4, e, n))
{
    Console.WriteLine("Измененная электронная подпись действительна.");
}
else
{
    Console.WriteLine("Измененная электронная подпись недействительна.");
}

using System;
using System.Numerics;
using System.Collections.Generic;


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
        if (lowPrimes[i] == prime)
            return true;
        if (prime % lowPrimes[i] == 0)
            return false;
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
            return false;
    }

    return true;
}

// генерирует БОЛЬШОЕ случайное число в заданном отрезке.
BigInteger RandBigIntegerInRange(BigInteger minValue, BigInteger maxValue)
{
    if (minValue == maxValue) return minValue;

    var random = new Random();
    BigInteger zeroBasedUpperBound = maxValue - 1 - minValue;
    byte[] bytes = zeroBasedUpperBound.ToByteArray();

    byte lastByteMask = 0b11111111;
    for (byte mask = 0b10000000; mask > 0; mask >>= 1, lastByteMask >>= 1)
        if ((bytes[bytes.Length - 1] & mask) == mask) break;

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
        int bits = 32;
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

// расширенный алгоритм Евклида. используется для нахождения обратного по модулю числа.
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

// функция поиска первообразного корня.
BigInteger GeneratePrimitiveRoot(BigInteger p)
{
    var f = new List<BigInteger>();
    var n = p - 1;
    for (var i = 2; i*i <= n; i++)
    {
        if (n % i == 0)
        {
            f.Add(i);
            while (n % i == 0)
                n = n / i;
        }
    }
    if (n != 1)
        f.Add(n);

    n = p - 1;
    for (var i = 2; i < p; i++)
    {
        bool flag = true;
        foreach (var k in f)
            flag = flag && (BinPow(i, n / k, p) != 1);

        if (flag)
            return i;
    }

    return 0;
}

// функция генерации ключей для схемы Эль-Гамаля.
void GenerateElgamalKeys(out BigInteger y, out BigInteger g, out BigInteger p, out BigInteger x)
{
    p = getRandomPrime();
    g = GeneratePrimitiveRoot(p);
    x = RandBigIntegerInRange(2, p - 2);
    y = BinPow(g, x, p);
}

// функция генерации цифровой подписи.
void GenerateCert(in BigInteger p, in BigInteger g, in BigInteger x, in BigInteger m, out BigInteger r, out BigInteger s)
{
    BigInteger k, k_inv;

    do
        k = RandBigIntegerInRange(2, p - 2); // случайное число k от 1 до n-1.
    while (GCD(k, p - 1) != 1); // k и n-1 должны быть взаимопростыми.

    r = BinPow(g, k, p); // r = g^k mod n.
    GCDex(k, p - 1, out k_inv, out BigInteger y); // k^-1 mod (n-1).

    k_inv = (k_inv % (p - 1) + (p - 1)) % (p - 1); // нужно, чтобы k_inv было в пределах от 0 до p-1.

    s = (m - x * r) * k_inv % (p - 1);
    s = (s % (p - 1) + (p - 1)) % (p - 1); // аналогично с k_inv.
}

// проверка цифровой подписи.
bool ValidateCert(BigInteger p, BigInteger g, BigInteger y, BigInteger m, BigInteger r, BigInteger s)
{
    if (r <= 0 || r >= p || s <= 0 || s >= p - 1) // 0<r<n и 0<s<n-1
        return false;

    var v1 = BinPow(y, r, p) * BinPow(r, s, p) % p;
    var v2 = BinPow(g, m, p);
    return v1 == v2;
}


BigInteger m = 1111; // сообщение.
BigInteger y, g, p, x;

GenerateElgamalKeys(out y, out g, out p, out x);

Console.WriteLine($"Открытый ключ: (n: {p}, g: {g}, y: {y})");
Console.WriteLine($"Закрытый ключ: (n: {p}, g: {g}, x: {x})");

GenerateCert(p, g, x, m, out var r, out var s);

Console.WriteLine($"Цифровая подпись: (r: {r}, s: {s})");

if (ValidateCert(p, g, y, m, r, s))
    Console.WriteLine("Цифровая подпись действительна.");
else
    Console.WriteLine("Цифровая подпись недействительна.");

if (ValidateCert(p, g, y, m, r + 4, s + 4))
    Console.WriteLine("Измененная цифровая подпись действительна.");
else
    Console.WriteLine("Измененная цифровая подпись недействительна.");

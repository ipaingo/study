using System.Numerics;
using System;
using System.Security.Cryptography;
using System.Runtime.CompilerServices;

// Function to calculate modular exponentiation
BigInteger BinPow(BigInteger n, BigInteger k, BigInteger mod)
{
    if (k == 0)
        return new BigInteger(1);
    if (k == 1)
        return n % mod;

    // Recursively compute the modular exponentiation
    var mid = BinPow(n, k / 2, mod);
    return mid * mid * (k % 2 == 1 ? n : 1) % mod;
}

// Function to generate a list of low prime numbers
List<int> generateLowPrimes()
{
    // Sieve of Eratosthenes algorithm to generate primes up to 2000
    bool[] sieve = new bool[2000];
    for (int i = 2; i < 2000; i++)
    {
        if (!sieve[i])
        {
            // Mark multiples of the current prime as non-prime
            for (int j = i * i; j < 2000; j += i)
            {
                sieve[j] = true;
            }
        }
    }

    // Collect the primes from the sieve
    var primes = new List<int>();
    for (int i = 2; i < 2000; i++)
    {
        if (!sieve[i])
        {
            primes.Add(i);
        }
    }

    return primes;
}

// Generate low prime numbers and store them for later use
var lowPrimes = generateLowPrimes();

// Function to probabilistically determine if a number is prime
bool isMayBePrime(BigInteger prime)
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

    // Miller-Rabin primality test for probable prime numbers
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

// Function to generate a random prime number
BigInteger getRandomPrime()
{
    while (true)
    {
        // Generate a random number and check if it's prime
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
        if (!isMayBePrime(prime))
            continue;
        return prime;
    }
}

// Function to calculate the greatest common divisor (GCD)
BigInteger GCD(BigInteger a, BigInteger b)
{
    // Euclidean algorithm to calculate GCD
    if (b > a)
        (a, b) = (b, a);
    while (b > 0)
    {
        a %= b;
        (a, b) = (b, a);
    }

    return a;
}

// Function to calculate the extended GCD
BigInteger GCDex(BigInteger a, BigInteger b, out BigInteger x, out BigInteger y)
{
    // Extended Euclidean algorithm to calculate GCD and coefficients
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

// Function to generate RSA public and private keys
void generateRSAKeys(BigInteger e, out BigInteger d, out BigInteger n, out BigInteger p, out BigInteger q)
{
    BigInteger f;
    do
    {
        // Generate random prime numbers p and q
        p = getRandomPrime();
        q = getRandomPrime();
        n = p * q;
        f = (p - 1) * (q - 1);
    } while (GCD(e, f) != 1);
    // Calculate private key d using extended Euclidean algorithm
    GCDex(e, f, out d, out BigInteger y);
    d = (d % f + f) % f;
}

// Function to generate a digital signature
BigInteger getCert(in BigInteger m, in BigInteger d, in BigInteger n)
{
    // Calculate digital signature using modular exponentiation
    return BinPow(m, d, n);
}

// Function to generate a digital signature faster using the Chinese Remainder Theorem
BigInteger getCertFast(in BigInteger m, in BigInteger d, in BigInteger n, in BigInteger p, in BigInteger q)
{
    // Calculate digital signature using the Chinese Remainder Theorem
    var r1 = BinPow(m % p, d % (p - 1), p);
    var r2 = BinPow(m % q, d % (q - 1), q);

    BigInteger m1, m2;
    GCDex(q, p, out m1, out BigInteger y1);
    GCDex(p, q, out m2, out BigInteger y2);
    m1 = (m1 % p + p) % p;
    m2 = (m2 % q + q) % q;

    return (r1 * m1 * q + r2 * m2 * p) % n;
}

// Function to validate a digital signature
bool validateCert(in BigInteger m, in BigInteger cert, in BigInteger e, BigInteger n)
{
    // Verify the digital signature
    return m == BinPow(cert, e, n);
}

// Main code execution
BigInteger m = 1111;
BigInteger e = 1337;
BigInteger n, d, p, q;
generateRSAKeys(e, out d, out n, out p, out q);

Console.WriteLine($"Public Key (n, e): ({n}, {e})");
Console.WriteLine($"Private Key (n, d): ({n}, {d})");

var cert = getCert(m, d, n);
var cert2 = getCertFast(m, d, n, p, q);

Console.WriteLine("Digital Signature:");
Console.WriteLine($"Using Standard Method: {cert}");
Console.WriteLine($"Using Chinese Remainder Theorem: {cert2}");

if (validateCert(m, cert, e, n))
{
    Console.WriteLine("Digital Signature is Valid");
}
else
{
    Console.WriteLine("Digital Signature is Invalid");
}

if (validateCert(m, cert + 4, e, n))
{
    Console.WriteLine("Modified Digital Signature is Valid");
}
else
{
    Console.WriteLine("Modified Digital Signature is Invalid");
}

// Function to generate a random BigInteger within a given range
BigInteger RandBigIntegerInRange(BigInteger minValue, BigInteger maxValue)
{
    if (minValue == maxValue) return minValue;
    var random = new Random();
    BigInteger zeroBasedUpperBound = maxValue - 1 - minValue; // Inclusive
    byte[] bytes = zeroBasedUpperBound.ToByteArray();

    // Search for the most significant non-zero bit
    byte lastByteMask = 0b11111111;
    for (byte mask = 0b10000000; mask > 0; mask >>= 1, lastByteMask >>= 1)
    {
        if ((bytes[bytes.Length - 1] & mask) == mask) break; // We found it
    }

    while (true)
    {
        random.NextBytes(bytes);
        bytes[bytes.Length - 1] &= lastByteMask;
        var result = new BigInteger(bytes);
        if (result <= zeroBasedUpperBound) return result + minValue;
    }
}

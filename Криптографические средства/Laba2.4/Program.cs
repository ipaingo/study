using System.Numerics;
using System;

BigInteger BinPow(BigInteger n, BigInteger k, BigInteger mod) {
    if (k == 0)
        return new BigInteger(1);
    if (k == 1)
        return n % mod;

    var mid = BinPow(n, k / 2, mod);
    return mid * mid * (k % 2 == 1 ? n : 1) % mod;
}

List<int> generateLowPrimes() {
    bool[] sieve = new bool[2000];
    for (int i = 2; i < 2000; i++) {
        if (!sieve[i]) {
            for (int j = i * i; j < 2000; j += i) {
                sieve[j] = true;
            }
        }
    }

    var primes = new List<int>();
    for (int i = 2; i < 2000; i++) {
        if (!sieve[i]) {
            primes.Add(i);
        }
    }

    return primes;
}

var lowPrimes = generateLowPrimes();

bool isMayBePrime(BigInteger prime) {
    foreach (var lp in lowPrimes) {
        if (lp == prime)
            return true;
        if (prime % lp == 0) {
            return false;
        }
    }

    int s = 0;
    BigInteger t = prime - 1;
    while (t % 2 == 0) {
        t /= 2;
        s++;
    }

    int iters = 256;
    while (iters-- > 0) {
        var a = RandBigIntegerInRange(2, prime - 2);
        var x = BinPow(a, t, prime);
        if (x == 1 || x == prime - 1)
            continue;

        bool flag = true;
        for (int i = 1; i < s; i++) {
            x = BinPow(x, 2, prime);
            if (x == 1)
                return false;
            if (x == prime - 1) {
                flag = false;
                break;
            }
        }
        if (flag) {
            return false;
        }
    }

    return true;
}

BigInteger getRandomPrime() {
    while (true) {
        int bits = 32;
        BigInteger min = 1, max = 2;
        while (--bits > 0) {
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


BigInteger GCD(BigInteger a, BigInteger b) {
    if (b > a)
        (a, b) = (b, a);
    while (b > 0) {
        a %= b;
        (a, b) = (b, a);
    }

    return a;
}

BigInteger GCDex(BigInteger a, BigInteger b, out BigInteger x, out BigInteger y) {
	if (a == 0) {
		x = 0; y = 1;
		return b;
	}
	BigInteger x1, y1;
	BigInteger d = GCDex(b % a, a, out x1, out y1);
	x = y1 - (b / a) * x1;
	y = x1;
	return d;
}



BigInteger GeneratePrimitiveRoot(BigInteger a) {
    var f = new List <BigInteger>();
    var p = a - 1;
    for (var i = 2; i * i <= p; i++) {
        if (p % i == 0) {
            f.Add(i);
            while (p % i == 0)
                p /= i;
        }
    }
    if (p != 1)
        f.Add(p);

    p = a - 1;
    for (var i = 2; i < a; i++) {
        bool flag = true;
        foreach (var k in f) {
            flag = flag && (BinPow(i, p / k, a) != -1);
        }
        if (flag)
            return i;
    }

    return 0;
}

void GenerateElGamalKeys(out BigInteger y, out BigInteger g, out BigInteger p, out BigInteger x) {
    p = getRandomPrime();
    g = GeneratePrimitiveRoot(p);
    x = RandBigIntegerInRange(2, p - 2);
    y = BinPow(g, x, p);
}

void GenerateCert(in BigInteger p, in BigInteger g, in BigInteger x, in BigInteger m, out BigInteger r, out BigInteger s) {
    BigInteger k, k_obr;
    do {
        k = RandBigIntegerInRange(2, p - 2);
    } while (GCD(k, p - 1) != 1);
    r = BinPow(g, k, p);
    GCDex(k, p - 1, out k_obr, out BigInteger y);
    k_obr = (k_obr % (p - 1) + (p - 1)) % (p - 1);
    s = (m - x * r) * k_obr % (p - 1);
    s = (s % (p - 1) + (p - 1)) % (p - 1);
}

bool ValidateCert(in BigInteger p, in BigInteger g, in BigInteger y, in BigInteger m, in BigInteger r, in BigInteger s) {
    if (r <= 0 || r >= p || s <= 0 || s >= p - 1)
        return false;

    return BinPow(y, r, p) * BinPow(r, s, p) % p == BinPow(g, m, p);
}



BigInteger m = 1111;
BigInteger y, g, p, x;

GenerateElGamalKeys(out y, out g, out p, out x);

Console.WriteLine($"({p}, {g}, {y})");
Console.WriteLine($"({p}, {g}, {x})");

BigInteger r, s;
GenerateCert(p, g, x, m, out r, out s);

Console.WriteLine($"({r}, {s})");

if (ValidateCert(p, g, y, m, r, s)) {
    Console.WriteLine("Valid");
} else {
    Console.WriteLine("Invalid");
}

if (ValidateCert(p, g, y, m, r + 4, s + 4)) {
    Console.WriteLine("Valid");
} else {
    Console.WriteLine("Invalid");
}


















BigInteger RandBigIntegerInRange(BigInteger minValue, BigInteger maxValue) {
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

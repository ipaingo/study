using System.Numerics;
using System;
using System.Text;
using System.Security.Cryptography;

// пути к папкам и файлам.
var mainDirectory = Directory.GetCurrentDirectory() + Path.DirectorySeparatorChar;
var aliceDirectory = mainDirectory + "Alice" + Path.DirectorySeparatorChar;
var bobDirectory = mainDirectory + "Bob" + Path.DirectorySeparatorChar;
var alicePublicKey = aliceDirectory + "PublicRSA.key";
var alicePrivateKey = aliceDirectory + "PrivateRSA.key";
var bobPublicKey = bobDirectory + "PublicRSA.key";
var bobPrivateKey = bobDirectory + "PrivateRSA.key";
var aliceMessageFile = aliceDirectory + "message.txt";
var aliceCertificate = aliceDirectory + "message.certificateToDecode";
var aliceMessageKey = aliceDirectory + "message.key";
var aliceEncoded = aliceDirectory + "encoded";
var bobDecoded = bobDirectory + "decoded.txt";

// функция для записи байтового массива в файл.
void WriteBytes(string filePath, byte[] bytes)
{
    using BinaryWriter writer = new(File.Open(filePath, FileMode.OpenOrCreate));
    writer.Write(bytes);
}

// функция для записи строки в файл.
void WriteString(string filePath, string str)
{
    using StreamWriter writer = new(File.Open(filePath, FileMode.OpenOrCreate));
    writer.Write(str);
}

// функция для генерации RSA ключей и записи их в файл.
void GenerateAndWriteRSAKeys(string publicKeyPath, string privateKeyPath)
{
    RSA rsa = RSA.Create();

    WriteBytes(publicKeyPath, rsa.ExportRSAPublicKey());
    WriteBytes(privateKeyPath, rsa.ExportRSAPrivateKey());
}

// функция для прочтения ключей из файла и записи их в RSA объект.
RSA ReadRSA(string publicKeyPath, string privateKeyPath)
{
    RSA rsa = RSA.Create();
    rsa.ImportRSAPublicKey(File.ReadAllBytes(publicKeyPath), out int k1);
    rsa.ImportRSAPrivateKey(File.ReadAllBytes(privateKeyPath), out int k2);

    return rsa;
}

// симметричное шифрование проводится с помощью алгоритма AES.
// это функция для генерации AES ключа.
Aes GenerateAes()
{
    Aes aes = Aes.Create();
    aes.GenerateKey();
    return aes;
}

// функция для чтения AES ключа из файла.
Aes ReadAes(string keyPath)
{
    Aes aes = Aes.Create();
    aes.Key = File.ReadAllBytes(keyPath);

    return aes;
}

// функция для шифрования сообщения.
void EncodeMessage(string message, Aes aes, RSA aliceRSA, RSA bobRSA, out byte[] encodedKey, out byte[] encodedMessage, out byte[] cert)
{
    // сначала шифруем сообщение с помощью AES.
    encodedMessage = aes.EncryptEcb(new UTF8Encoding().GetBytes(message), PaddingMode.ANSIX923);
    // сам ключ AES шифруется с помощью RSA.
    encodedKey = bobRSA.Encrypt(aes.Key, RSAEncryptionPadding.OaepSHA256);
    // цифровая подпись с помощью RSA.
    cert = aliceRSA.SignData(new UTF8Encoding().GetBytes(message), HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
}

// функция для расшифровки сообщения.
void DecodeMessage(RSA aliceRSA, RSA bobRSA, byte[] encodedMessage, byte[] encodedKey, out byte[] originalMessage)
{
    Aes aes = Aes.Create();
    // расшифровка AES ключа с помощью RSA.
    aes.Key = bobRSA.Decrypt(encodedKey, RSAEncryptionPadding.OaepSHA256);
    // расшифровка сообщения с помощью AES ключа.
    originalMessage = aes.DecryptEcb(encodedMessage, PaddingMode.ANSIX923);
}

// функция проверки цифровой подписи.
bool VerifyMessage(RSA aliceRSA, byte[] message, byte[] cert)
{
    return aliceRSA.VerifyData(message, cert, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
}


void MainLogic()
{
    // генерация RSA ключей.
    if (!File.Exists(alicePublicKey) || !File.Exists(alicePrivateKey))
        GenerateAndWriteRSAKeys(alicePublicKey, alicePrivateKey);

    if (!File.Exists(bobPublicKey) || !File.Exists(bobPrivateKey))
        GenerateAndWriteRSAKeys(bobPublicKey, bobPrivateKey);

    // чтение RSA ключей из файлов.
    var aliceRSA = ReadRSA(alicePublicKey, alicePrivateKey);
    var bobRSA = ReadRSA(bobPublicKey, bobPrivateKey);

    // чтение сообщения из файла.
    var aliceMessage = File.ReadAllText(aliceMessageFile);



    // шифрование и подпись.
    Aes aes = GenerateAes();
    EncodeMessage(aliceMessage, aes, aliceRSA, bobRSA, out byte[] encodedKey, out byte[] encodedMessage, out byte[] certificate);

    WriteBytes(aliceEncoded, encodedMessage);
    WriteBytes(aliceMessageKey, encodedKey);
    WriteBytes(aliceCertificate, certificate);


    // расшифровка и проверка подписи.
    byte[] encodedMessageToDecode = File.ReadAllBytes(aliceEncoded);
    byte[] encodedKeyToDecode = File.ReadAllBytes(aliceMessageKey);
    byte[] certificateToDecode = File.ReadAllBytes(aliceCertificate);
    byte[] originalMessage;

    DecodeMessage(aliceRSA, bobRSA, encodedMessageToDecode, encodedKeyToDecode, out originalMessage);
    WriteString(bobDecoded, new UTF8Encoding().GetString(originalMessage));

    bool dataVerified = VerifyMessage(aliceRSA, originalMessage, certificateToDecode);

    Console.WriteLine(dataVerified);
}

MainLogic();
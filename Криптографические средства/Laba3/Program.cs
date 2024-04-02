using System.Numerics;
using System;
using System.Text;
using System.Security.Cryptography;

var mainDirPath = Directory.GetCurrentDirectory() + Path.DirectorySeparatorChar;
var dirAlicePath = mainDirPath + "Alice" + Path.DirectorySeparatorChar;
var dirBobPath = mainDirPath + "Bob" + Path.DirectorySeparatorChar;
var fileAlicePublicKeyPath          = dirAlicePath + "PublicRSA.key";
var fileAlicePrivateKeyPath         = dirAlicePath + "PrivateRSA.key";
var fileBobPublicKeyPath            = dirBobPath + "PublicRSA.key";
var fileBobPrivateKeyPath           = dirBobPath + "PrivateRSA.key";
var fileAliceOriginalMessagePath    = dirAlicePath + "message.txt";
var fileAliceMessageCertPath        = dirAlicePath + "message.cert";
var fileAliceMessageKeyPath        = dirAlicePath + "message.key";
var fileAliceEncodedMessagePath     = dirAlicePath + "encoded";
var fileBobDecodedMessagePath       = dirBobPath + "decoded.txt";

void WriteBytes(string filePath, byte[] bytes) {
    using BinaryWriter writer = new(File.Open(filePath, FileMode.OpenOrCreate));
    writer.Write(bytes);
}

void WriteString(string filePath, string str) {
    using StreamWriter writer = new(File.Open(filePath, FileMode.OpenOrCreate));
    writer.Write(str);
}

void GenerateAndWriteRSAKeys(string publicKeyPath, string privateKeyPath) {
    RSA rsa = RSA.Create();

    WriteBytes(publicKeyPath, rsa.ExportRSAPublicKey());
    WriteBytes(privateKeyPath, rsa.ExportRSAPrivateKey());
}

RSA ReadRSA(string publicKeyPath, string privateKeyPath) {
    RSA rsa = RSA.Create();
    rsa.ImportRSAPublicKey(File.ReadAllBytes(publicKeyPath), out int k1);
    rsa.ImportRSAPrivateKey(File.ReadAllBytes(privateKeyPath), out int k2);

    return rsa;
}

Aes GenerateAes() {
    Aes aes = Aes.Create();
    aes.GenerateKey();
    return aes;
}

Aes ReadAes(string keyPath) {
    Aes aes = Aes.Create();
    aes.Key = File.ReadAllBytes(keyPath);

    return aes;
}

void EncodeMessage(string message, Aes aes, RSA aliceRSA, RSA bobRSA, out byte[] encodedKey, out byte[] encodedMessage, out byte[] cert) {
    encodedMessage = aes.EncryptEcb(new UTF8Encoding().GetBytes(message), PaddingMode.ANSIX923);
    encodedKey = bobRSA.Encrypt(aes.Key, RSAEncryptionPadding.OaepSHA256);
    cert = aliceRSA.SignData(new UTF8Encoding().GetBytes(message), HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
}

void DecodeMessage(RSA aliceRSA, RSA bobRSA, byte[] encodedMessage, byte[] encodedKey, out byte[] originalMessage) {
    Aes aes = Aes.Create();
    aes.Key = bobRSA.Decrypt(encodedKey, RSAEncryptionPadding.OaepSHA256);
    originalMessage = aes.DecryptEcb(encodedMessage, PaddingMode.ANSIX923);
}

bool VerifyMessage(RSA aliceRSA, byte[] message, byte[] cert) {
    return aliceRSA.VerifyData(message, cert, HashAlgorithmName.SHA256, RSASignaturePadding.Pss);
}





{
    if (!File.Exists(fileAlicePublicKeyPath) || !File.Exists(fileAlicePrivateKeyPath)) {
        GenerateAndWriteRSAKeys(fileAlicePublicKeyPath, fileAlicePrivateKeyPath);
    }

    if (!File.Exists(fileBobPublicKeyPath) || !File.Exists(fileBobPrivateKeyPath)) {
        GenerateAndWriteRSAKeys(fileBobPublicKeyPath, fileBobPrivateKeyPath);
    }

    var aliceRSA = ReadRSA(fileAlicePublicKeyPath, fileAlicePrivateKeyPath);
    var bobRSA = ReadRSA(fileBobPublicKeyPath, fileBobPrivateKeyPath);

    var aliceMessage = File.ReadAllText(fileAliceOriginalMessagePath);

    // Шифрование и подпись
    {
        Aes aes = GenerateAes();
        EncodeMessage(aliceMessage, aes, aliceRSA, bobRSA, out byte[] encodedKey, out byte[] encodedMessage, out byte[] cert);

        WriteBytes(fileAliceEncodedMessagePath, encodedMessage);
        WriteBytes(fileAliceMessageKeyPath, encodedKey);
        WriteBytes(fileAliceMessageCertPath, cert);
    }

    // Дешифрование и проверка подписи
    {
        byte[] encodedMessage = File.ReadAllBytes(fileAliceEncodedMessagePath);
        byte[] encodedKey = File.ReadAllBytes(fileAliceMessageKeyPath);
        byte[] cert = File.ReadAllBytes(fileAliceMessageCertPath);
        byte[] originalMessage;

        DecodeMessage(aliceRSA, bobRSA, encodedMessage, encodedKey, out originalMessage);
        WriteString(fileBobDecodedMessagePath, new UTF8Encoding().GetString(originalMessage));

        bool dataVerified = VerifyMessage(aliceRSA, originalMessage, cert);

        Console.WriteLine(dataVerified);
    }
}

using System;
using System.Collections.Generic;
using System.Linq;

namespace func.brainfuck
{
    public class BrainfuckBasicCommands
    {
        public static void RegisterTo(IVirtualMachine vm, Func<int> read, Action<char> write)
        {
            vm.RegisterCommand('.', b => { write((char)b.Memory[b.MemoryPointer]); }); // ����� �� ������.
            vm.RegisterCommand('+', b => { b.Memory[b.MemoryPointer]++; }); // ++.
            vm.RegisterCommand('-', b => { b.Memory[b.MemoryPointer]--; }); // --.
            vm.RegisterCommand(',', b => { b.Memory[b.MemoryPointer] = (byte)read(); }); // ���� � ������.

            vm.RegisterCommand('>', b =>
            {
                // ���������, ������ �� ������ �� ������� ���������� ������.
                if (b.MemoryPointer + 1 > b.Memory.Length)
                    // ���� ��, �������� � ������ � ������ �� �����.
                    b.MemoryPointer = 0;
                else
                    b.MemoryPointer = b.MemoryPointer + 1;

            }); // �������� ��������� ������.

            vm.RegisterCommand('<', b =>
            {
                if (b.MemoryPointer - 1 < 0)
                    b.MemoryPointer = b.Memory.Length - 1;
                else
                    b.MemoryPointer = b.MemoryPointer - 1;

            }); // �������� ��������� �����.

            // ��� ���� ��������� ��������.
            string alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
            foreach (char c in alphabet)
            {
                vm.RegisterCommand(c, b => { b.Memory[b.MemoryPointer] = (byte)c; });
                // ��������� � ��� ������ ��� �������.
            }
        }
    }
}

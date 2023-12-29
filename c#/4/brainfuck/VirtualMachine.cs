using System;
using System.Collections.Generic;

namespace func.brainfuck
{
	public class VirtualMachine : IVirtualMachine
	{
		public string Instructions { get; }
		public int InstructionPointer { get; set; }
		public byte[] Memory { get; }
		public int MemoryPointer { get; set; }

        private Dictionary<char, Action<IVirtualMachine>> bfCommands; // �������-������ - ��������-������-��-�������.

        public VirtualMachine(string program, int memorySize)
		{
			Instructions = program; // ����� visual studio �� ��,
			InstructionPointer = 0; // ��� ��� ����� ��� �� ����.
            Memory = new byte[memorySize];
			MemoryPointer = 0;
			bfCommands = new Dictionary<char, Action<IVirtualMachine>>();
		}

		public void RegisterCommand(char symbol, Action<IVirtualMachine> execute)
		{
			bfCommands[symbol] = execute;
		}

		public void Run()
		{
			while (InstructionPointer < Instructions.Length) // �������� �� �����������.
			{
				char instructionChar = Instructions[InstructionPointer];
				if (bfCommands.ContainsKey(instructionChar)) // ���� ����� ������� ���� � ������,
				{
					bfCommands[instructionChar](this); // �� ��������� ��. ���� ������, ��������� ������� �� �������� �������.
				}
				InstructionPointer++; // ���� � ��������� �������.
			}
		}
	}
}

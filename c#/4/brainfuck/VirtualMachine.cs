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

        private Dictionary<char, Action<IVirtualMachine>> bfCommands; // команда-символ - действие-ссылка-на-функцию.

        public VirtualMachine(string program, int memorySize)
		{
			Instructions = program; // люблю visual studio за то,
			InstructionPointer = 0; // что она пишет код за меня.
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
			while (InstructionPointer < Instructions.Length) // проходим по инструкциям.
			{
				char instructionChar = Instructions[InstructionPointer];
				if (bfCommands.ContainsKey(instructionChar)) // если такая команда есть в списке,
				{
					bfCommands[instructionChar](this); // то исполняем ее. если точнее, исполняем функцию от текущего объекта.
				}
				InstructionPointer++; // идем к следующей команде.
			}
		}
	}
}

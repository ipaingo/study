using System;
using System.Collections.Generic;

namespace Antiplagiarism
{
    public static class LongestCommonSubsequenceCalculator
    {
        public static List<string> Calculate(List<string> firstSequence, List<string> secondSequence)
        {
            int[,] opt = new int[firstSequence.Count + 1, secondSequence.Count + 1];

            // Инициализация массива opt
            for (int i = 0; i <= firstSequence.Count; i++)
                opt[i, 0] = 0;
            for (int j = 0; j <= secondSequence.Count; j++)
                opt[0, j] = 0;

            // Заполнение массива opt
            for (int i = 1; i <= firstSequence.Count; i++)
                for (int j = 1; j <= secondSequence.Count; j++)
                {
                    if (firstSequence[i - 1] == secondSequence[j - 1])
                        opt[i, j] = opt[i - 1, j - 1] + 1;
                    else
                        opt[i, j] = Math.Max(opt[i, j - 1], opt[i - 1, j]);
                }

            return GetBackTrack(opt, firstSequence, secondSequence, firstSequence.Count, secondSequence.Count);
        }

        private static List<string> GetBackTrack(int[,] opt, List<string> first, List<string> second, int x, int y)
        {
            if (x == 0 | y == 0)
                return new List<string>();
            if (first[x - 1] == second[y - 1])
            {
                // Рекурсивный возврат по пути
                var result = GetBackTrack(opt, first, second, x - 1, y - 1);
                result.Add(first[x - 1]);
                return result;
            }

            if (opt[x, y - 1] > opt[x - 1, y])
                return GetBackTrack(opt, first, second, x, y - 1);

            return GetBackTrack(opt, first, second, x - 1, y);
        }

        private static int[,] CreateOptimizationTable(List<string> first, List<string> second)
        {
            throw new NotImplementedException();
        }

        private static List<string> RestoreAnswer(int[,] opt, List<string> first, List<string> second)
        {
            throw new NotImplementedException();
        }
    }
}

using System;
using System.Collections.Generic;

namespace Antiplagiarism
{
    public static class LongestCommonSubsequenceCalculator
    {
        public static List<string> Calculate(List<string> first, List<string> second)
        {
            var table = CreateOptimizationTable(first, second);
            var ans = RestoreAnswer(table, first, second);
            ans.Reverse();

            return ans;
        }

        private static int[,] CreateOptimizationTable(List<string> first, List<string> second)
        {
            var table = new int[first.Count + 1, second.Count + 1]; // состояние.
            // база. работает и без нее (нули все-таки),
            // но вдруг там окажется какой-нибудь мусор - лучше все же очистить.
            for (int i = 0; i <= first.Count; i++)
                table[i, 0] = 0;
            for (int i = 0; i <= second.Count; i++)
                table[0, i] = 0;

            for (int i = 1; i <= first.Count; i++) // порядок пересчета.
                for (int j = 1; j <= second.Count; j++)
                {   // переход.
                    int match = 0;
                    if (first[i - 1] == second[j - 1])
                        match = 1;
                    table[i, j] = Math.Max(Math.Max(table[i - 1, j], table[i, j - 1]), table[i - 1, j - 1] + match);
                }
            // ответ.
            return table;
        }

        private static List<string> RestoreAnswer(int[,] table, List<string> first, List<string> second)
        {
            var ans = new List<string>();
            // идем в обратном порядке, по таблице восстанавливая наибольшую общую последовательность.
            // как с Левенштейном получается...
            for (int i = first.Count, j = second.Count; i > 0 && j > 0;)
                if (first[i - 1] == second[j - 1])
                {
                    ans.Add(first[i - 1]);
                    i = i - 1;
                    j = j - 1;
                }
                else if (table[i - 1, j] > table[i, j - 1])
                    i = i - 1;
                else
                    j = j - 1;

            return ans;
        }
    }
}

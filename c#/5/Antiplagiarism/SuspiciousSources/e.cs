using System;
using System.Collections.Generic;

namespace Antiplagiarism;

public static class LongestCommonSubsequenceCalculator
{
	public static List<string> Calculate(List<string> first, List<string> second) {
		var opt = CreateOptimizationTable(first, second);
		return RestoreAnswer(opt, first, second);
	}

	private static int[,] CreateOptimizationTable(List<string> first, List<string> second) {
		var table = new int[first.Count + 1, second.Count + 1];
		for (int i = 0; i <= first.Count; i++)
			table[i, 0] = 0;
		for (int i = 0; i <= second.Count; i++)
			table[0, i] = 0;

		for (int i = 1; i <= first.Count; i++) {
			for (int j = 1; j <= second.Count; j++) {
				table[i, j] = Math.Max(Math.Max(table[i - 1, j], table[i, j - 1]), table[i - 1, j - 1] + (first[i - 1] == second[j - 1] ? 1 : 0));
			}
		}

		return table;
	}

	private static List<string> RestoreAnswer(int[,] opt, List<string> first, List<string> second) {
		var ans = new List<string>();
		int i = first.Count;
		int j = second.Count;
		while (i != 0 && j != 0) {
			if (opt[i, j - 1] == opt[i, j]) {
				j--;
			} else
			if (opt[i - 1, j] == opt[i, j]) {
                i--;
            } else {
                ans.Add(first[i - 1]);
                i--;
				j--;
            }
        }
		ans.Reverse();

        return ans;
	}
}
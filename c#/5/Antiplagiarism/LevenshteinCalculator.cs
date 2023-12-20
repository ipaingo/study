using System;
using System.Collections.Generic;

// Каждый документ — это список токенов. То есть List<string>.
// Вместо этого будем использовать псевдоним DocumentTokens.
// Это поможет избежать сложных конструкций:
// вместо List<List<string>> будет List<DocumentTokens>
using DocumentTokens = System.Collections.Generic.List<string>;

namespace Antiplagiarism
{
    public class LevenshteinCalculator
    {
        // сравнивает документы попарно.
        public List<ComparisonResult> CompareDocumentsPairwise(List<DocumentTokens> documents)
        {
            var results = new List<ComparisonResult>();

            // пробегаемся по всем документам.
            for (int i = 0; i < documents.Count; i++)
            {
                var first = documents[i]; // текущий документ.

                // сравниваем текущий документ со всеми остальными.
                for (int j = i + 1; j < documents.Count; j++)
                {
                    var second = documents[j];
                    // так, может, и длиннее, но зато читаемо.
                    var distance = CalculateLevenshteinDistance(first, second);
                    // результат в список ответов.
                    results.Add(new ComparisonResult(first, second, distance));
                }
            }

            return results;
        }

        // вычисляет расстояние Левенштейна.
        private double CalculateLevenshteinDistance(List<string> first, List<string> second)
        {
            // состояние. здесь будем хранить расстояния.
            var opt = new double[first.Count + 1, second.Count + 1];

            for (var i = 0; i <= first.Count; i++)      // база.
                opt[i, 0] = i;
            for (var i = 0; i <= second.Count; i++)
                opt[0, i] = i;

            for (var i = 1; i <= first.Count; i++)      // порядок пересчета.
                for (var j = 1; j <= second.Count; j++)
                {   // переход.
                    if (first[i - 1] == second[j - 1])  // если равны,
                        opt[i, j] = opt[i - 1, j - 1];  // действия не требуются.
                    else
                        opt[i, j] = Math.Min(1 + opt[i - 1, j], // по формуле ДП для поиска расстояния Левенштейна.
                            Math.Min(1 + opt[i, j - 1], opt[i - 1, j - 1] +
                            TokenDistanceCalculator.GetTokenDistance(first[i - 1], second[j - 1]))
                            );
                }
            // ответ.
            return opt[first.Count, second.Count];
        }
    }
}

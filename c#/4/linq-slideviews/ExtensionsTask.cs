using System;
using System.Collections.Generic;
using System.Linq;

namespace linq_slideviews;

public static class ExtensionsTask
{
    /// <summary>
	/// Медиана списка из нечетного количества элементов — это серединный элемент списка после сортировки.
	/// Медиана списка из четного количества элементов — это среднее арифметическое
    /// двух серединных элементов списка после сортировки.
	/// </summary>
	/// <exception cref="InvalidOperationException">Если последовательность не содержит элементов</exception>
    public static double Median(this IEnumerable<double> items)
    {
        // сортируем элементы и преобразовываем в массив.
        var sorted = items.OrderBy(item => item).ToArray();

        // отсортированный массив - не ienumerable, можно и на длину теперь посмотреть.
        if (sorted.Length == 0)
            throw new InvalidOperationException();

        // медиана - либо серединный элемент, либо среднее между двумя серединными элементами.
        if (sorted.Length % 2 == 0)
            return (sorted[sorted.Length / 2] + sorted[(sorted.Length - 1) / 2]) / 2;
        return sorted[sorted.Length / 2];
    }

    /// <returns>
	/// Возвращает последовательность, состоящую из пар соседних элементов.
	/// Например, по последовательности {1,2,3} метод должен вернуть две пары: (1,2) и (2,3).
	/// </returns>
    public static IEnumerable<(T First, T Second)> Bigrams<T>(this IEnumerable<T> items)
    {
        var prev = default(T); // потом, конечно, сразу положим туда элемент, но создать надо.
        bool first = true;

        // рассматриваем каждый элемент в последовательности.
        foreach (var item in items)
        {
            // если рассматриваемый элемент будет самым первым,
            // то запишем его, как первый в паре, и пойдем к следующему.
            if (first)
            {
                prev = item;
                first = false;
                continue;
            }
            // если рассматриваемый элемент второй, то мы вернем пару.
            yield return (prev, item);
            // далее мы просто будем все время возвращать предыдущий элемент и нынешний.
            prev = item;
        }
    }
}

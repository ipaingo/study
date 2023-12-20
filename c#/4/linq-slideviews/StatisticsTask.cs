using System;
using System.Collections.Generic;
using System.Linq;

namespace linq_slideviews;

public class StatisticsTask
{
    public static double GetMedianTimePerSlide(List<VisitRecord> visits, SlideType slideType)
    {
        var result = visits
            .GroupBy(visit => visit.UserId) // группируем по пользователям;

            .SelectMany(group => group
                .OrderBy(x => x.DateTime) // в каждой группе сортируем по времени,
                .Bigrams() // получаем биграммы,
                .Where(x => x.First.SlideType == slideType)) // оставляем только те, где тип слайда подходит,

            // и еще где время между минутой и двумя часами,
            .Where(x => x.Second.DateTime.Subtract(x.First.DateTime).TotalMinutes >= 1
                     && x.Second.DateTime.Subtract(x.First.DateTime).TotalMinutes <= 120)
            .Select(x => x.Second.DateTime.Subtract(x.First.DateTime).TotalMinutes)

            .ToList(); // и превращаем в список.

        // ноль, если ничего не подходит.
        if (result.Count == 0)
            return 0;

        // иначе возвращаем медиану.
        return result.Median();
    }
}
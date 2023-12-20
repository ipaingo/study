using System.Collections.Generic;

namespace yield;

public static class ExpSmoothingTask
{
	public static IEnumerable<DataPoint> SmoothExponentialy(this IEnumerable<DataPoint> data, double alpha)
	{
        DataPoint prev_point = null; // изначальна€ точка не имеет предыдущей точки.
        foreach (DataPoint point in data)
        {
            if (prev_point != null)
            {
                yield return prev_point = point.WithExpSmoothedY(alpha * point.OriginalY + (1 - alpha) * prev_point.ExpSmoothedY);
                                         // по формуле умножаем alpha на изначальную точку + (1-alpha) * предыдущую сглаженную точку.
            }
            else
            {
                yield return prev_point = point.WithExpSmoothedY(point.OriginalY);
                                          // а иначе это перва€ точка и надо просто вернуть изначальное значение.
            }
        }
    }
}

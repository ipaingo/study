using System.Collections.Generic;

namespace yield;

public static class MovingAverageTask
{
	public static IEnumerable<DataPoint> MovingAverage(this IEnumerable<DataPoint> data, int windowWidth)
	{
        double sum = 0;
        double k = 0;
        var queue = new Queue<DataPoint>();
        foreach (DataPoint point in data)
        {
            // нам нужны last k entries. будем добавлять их в очередь и считать сумму этой очереди.
            queue.Enqueue(point);
            k++;

            // прибавляем к сумме текущий элемент.
            sum += point.OriginalY;

            // без этой проверки работает плохо.
            // мы считаем среднее на промежутке - ширине окна.
            // если чисел многовато, просто уберем из нашей очереди (промежутка) самое старое.
            if (k > windowWidth)
            {
                sum -= queue.Dequeue().OriginalY;
                k--;
            }

            // по формуле сумму надо делить на количество.
            var sma = point.WithAvgSmoothedY(sum/k);

            yield return sma;
        }
    }
}
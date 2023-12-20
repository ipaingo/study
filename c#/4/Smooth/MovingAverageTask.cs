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
            // ��� ����� last k entries. ����� ��������� �� � ������� � ������� ����� ���� �������.
            queue.Enqueue(point);
            k++;

            // ���������� � ����� ������� �������.
            sum += point.OriginalY;

            // ��� ���� �������� �������� �����.
            // �� ������� ������� �� ���������� - ������ ����.
            // ���� ����� ���������, ������ ������ �� ����� ������� (����������) ����� ������.
            if (k > windowWidth)
            {
                sum -= queue.Dequeue().OriginalY;
                k--;
            }

            // �� ������� ����� ���� ������ �� ����������.
            var sma = point.WithAvgSmoothedY(sum/k);

            yield return sma;
        }
    }
}
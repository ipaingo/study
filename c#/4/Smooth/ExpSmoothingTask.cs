using System.Collections.Generic;

namespace yield;

public static class ExpSmoothingTask
{
	public static IEnumerable<DataPoint> SmoothExponentialy(this IEnumerable<DataPoint> data, double alpha)
	{
        DataPoint prev_point = null; // ����������� ����� �� ����� ���������� �����.
        foreach (DataPoint point in data)
        {
            if (prev_point != null)
            {
                yield return prev_point = point.WithExpSmoothedY(alpha * point.OriginalY + (1 - alpha) * prev_point.ExpSmoothedY);
                                         // �� ������� �������� alpha �� ����������� ����� + (1-alpha) * ���������� ���������� �����.
            }
            else
            {
                yield return prev_point = point.WithExpSmoothedY(point.OriginalY);
                                          // � ����� ��� ������ ����� � ���� ������ ������� ����������� ��������.
            }
        }
    }
}

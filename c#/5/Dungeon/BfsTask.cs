using System;
using System.Collections.Generic;
using System.Linq;

namespace Dungeon;

public class BfsTask
{
    public static IEnumerable<SinglyLinkedList<Point>> FindPaths(Map map, Point start, Point[] chests)
    {
        var queue = new Queue<(Point, SinglyLinkedList<Point>)>();
        queue.Enqueue((start, new SinglyLinkedList<Point>(start)));

        // ��� ������ ����� ����� ����������, ��� �� ��� ����.
        var was = new HashSet<Point>();
        was.Add(start);

        var paths = new Dictionary<Point, SinglyLinkedList<Point>>();
        bool found = false;
        while (queue.Count > 0)
        {
            var dequeued = queue.Dequeue(); // �������������� �������� ����������, �������.
            var point = dequeued.Item1;
            var previous = dequeued.Item2;


            paths[point] = previous;
            Point newPoint;

            // ��� �������� �� ���� ��� ������ �� ���� ������������ (����� � ������)
            // ����� ���������, ��� �� � ���� ����� ��� �� ����,
            // ��� ��� ������ (���� ����� ������), � ��� ��� ������ �� �����.

            newPoint = new Point(point.X + 1, point.Y);
            if (!was.Contains(newPoint) && map.InBounds(newPoint) && map.Dungeon[newPoint.X, newPoint.Y] == MapCell.Empty)
            {
                was.Add(newPoint);
                queue.Enqueue((newPoint, new SinglyLinkedList<Point>(newPoint, previous)));
                if (chests.Contains(newPoint)) found = true;
            }

            newPoint = new Point(point.X, point.Y + 1);
            if (!was.Contains(newPoint) && map.InBounds(newPoint) && map.Dungeon[newPoint.X, newPoint.Y] == MapCell.Empty)
            {
                was.Add(newPoint);
                queue.Enqueue((newPoint, new SinglyLinkedList<Point>(newPoint, previous)));
                if (chests.Contains(newPoint)) found = true;
            }

            newPoint = new Point(point.X - 1, point.Y);
            if (!was.Contains(newPoint) && map.InBounds(newPoint) && map.Dungeon[newPoint.X, newPoint.Y] == MapCell.Empty)
            {
                was.Add(newPoint);
                queue.Enqueue((newPoint, new SinglyLinkedList<Point>(newPoint, previous)));
                if (chests.Contains(newPoint)) found = true;
            }

            newPoint = new Point(point.X, point.Y - 1);
            if (!was.Contains(newPoint) && map.InBounds(newPoint) && map.Dungeon[newPoint.X, newPoint.Y] == MapCell.Empty)
            {
                was.Add(newPoint);
                queue.Enqueue((newPoint, new SinglyLinkedList<Point>(newPoint, previous)));
                if (chests.Contains(newPoint)) found = true;
            }
        }
        //Console.WriteLine(found);

        foreach (var chest in chests)
        {
            if (paths.ContainsKey(chest))
                yield return paths[chest];
            else
                yield break;
                //yield return new SinglyLinkedList<Point>(start);
        }
    }
}
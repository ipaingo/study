using System;
using System.Collections.Generic;
using System.Linq;
using Greedy.Architecture;

namespace Greedy;

public class DijkstraPathFinder
{
    public IEnumerable<PathWithCost> GetPathsByDijkstra(State state, Point start, IEnumerable<Point> targets)
    {
        // ����� ������������ ������� � �����������. ����� ������� �� ������ ���������� ���� � ���������� ������.
        var queue = new PriorityQueue<(Point Current, Point Previous, int Cost, int Length), int>();
        var visited = new HashSet<Point>();

        // ������... � ������...
        queue.Enqueue((start, start, 0, 1), 0);
        visited.Add(start);

        var prevPoints = new Dictionary<Point, (Point Previous, int Cost, int Length)>();

        while (queue.Count > 0)
        {
            // ������������� ������� ������.
            var node = queue.Dequeue();

            prevPoints[node.Current] = (node.Previous, node.Cost, node.Length);

            // ���� �� ����� �� ������� - ���������� �������.
            if (state.IsChestAt(node.Current) && targets.Contains(node.Current))
            {
                var currentPoint = prevPoints[node.Current];
                var currentCost = currentPoint.Cost;
                var currentLength = currentPoint.Length;
                var pathList = new Point[currentLength];
                pathList[0] = node.Current;
                // ��� ����� ��������������� �������, �� ������� ������ � ���� ������,
                // � ���������� ���������� ������ � ������������ ����.
                for (int i = 1; i < currentLength; i++)
                {
                    pathList[i] = currentPoint.Previous;
                    currentPoint = prevPoints[currentPoint.Previous];
                }

                yield return new PathWithCost(currentCost, pathList.Reverse().ToArray());
            }
            // � ���� ���� �����?
            Point[] moves = new Point[] { new Point(-1, 0), new Point(1, 0), new Point(0, -1), new Point(0, 1) };
            // ��������� ��� ���� �����������.
            for (int i = 0; i < 4; i++)
            {
                // ���������, ��� ���� ����� ����, � ��� �� ��� ��� �� ����.
                var next = node.Current + moves[i];
                if (state.InsideMap(next) && !state.IsWallAt(next) && !visited.Contains(next))
                {
                    // ����������, ��� ����, ������ � ������� � ����������� ����������.
                    visited.Add(next);
                    queue.Enqueue((next, node.Current, node.Cost + state.CellCost[next.X, next.Y], node.Length + 1), node.Cost + state.CellCost[next.X, next.Y]);
                }
            }
        }
    }
}

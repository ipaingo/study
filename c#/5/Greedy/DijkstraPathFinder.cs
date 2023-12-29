using System;
using System.Collections.Generic;
using System.Linq;
using Greedy.Architecture;

namespace Greedy;

public class DijkstraPathFinder
{
    public IEnumerable<PathWithCost> GetPathsByDijkstra(State state, Point start, IEnumerable<Point> targets)
    {
        // будем использовать очередь с приоритетом. таким образом мы сможем определять путь с наименьшей длиной.
        var queue = new PriorityQueue<(Point Current, Point Previous, int Cost, int Length), int>();
        var visited = new HashSet<Point>();

        // начнем... с начала...
        queue.Enqueue((start, start, 0, 1), 0);
        visited.Add(start);

        var prevPoints = new Dictionary<Point, (Point Previous, int Cost, int Length)>();

        while (queue.Count > 0)
        {
            // рассматриваем текущую ячейку.
            var node = queue.Dequeue();

            prevPoints[node.Current] = (node.Previous, node.Cost, node.Length);

            // если мы дошли до сундука - возвращаем маршрут.
            if (state.IsChestAt(node.Current) && targets.Contains(node.Current))
            {
                var currentPoint = prevPoints[node.Current];
                var currentCost = currentPoint.Cost;
                var currentLength = currentPoint.Length;
                var pathList = new Point[currentLength];
                pathList[0] = node.Current;
                // для этого восстанавливаем цепочку, по которой пришли к этой клетке,
                // и возвращаем полученный список в перевернутом виде.
                for (int i = 1; i < currentLength; i++)
                {
                    pathList[i] = currentPoint.Previous;
                    currentPoint = prevPoints[currentPoint.Previous];
                }

                yield return new PathWithCost(currentCost, pathList.Reverse().ToArray());
            }
            // а куда идти можно?
            Point[] moves = new Point[] { new Point(-1, 0), new Point(1, 0), new Point(0, -1), new Point(0, 1) };
            // проделаем для всех направлений.
            for (int i = 0; i < 4; i++)
            {
                // проверяем, что туда можно идти, и что мы там еще не были.
                var next = node.Current + moves[i];
                if (state.InsideMap(next) && !state.IsWallAt(next) && !visited.Contains(next))
                {
                    // записываем, что были, кладем в очередь с обновленной стоимостью.
                    visited.Add(next);
                    queue.Enqueue((next, node.Current, node.Cost + state.CellCost[next.X, next.Y], node.Length + 1), node.Cost + state.CellCost[next.X, next.Y]);
                }
            }
        }
    }
}

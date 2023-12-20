using System;
using System.Collections.Generic;
using System.Linq;

namespace Dungeon;

public class DungeonTask
{
    // преобразует полученный поиском список в массив перемещений персонажа.
    public static MoveDirection[] pathToMoveArray(List<Point> list)
    {
        var path = new MoveDirection[list.Count - 1];

        for (int i = 1; i < list.Count; i++)
        {
            var direction = list[i] - list[i - 1];
            path[i - 1] = Walker.ConvertOffsetToDirection(direction);
        }

        return path;
    }

    public static MoveDirection[] FindShortestPath(Map map)
    {
        // по совету из подсказки.
        var fromStart = BfsTask.FindPaths(map, map.InitialPosition, map.Chests).ToList();
        var fromExit = BfsTask.FindPaths(map, map.Exit, map.Chests).ToList();
        var startExit = BfsTask.FindPaths(map, map.Exit, new Point[] { map.InitialPosition });

        // нужно убедиться, что поиски ведут к одному и тому же сундуку.
        fromStart.Sort((a, b) => { return a.Last().ToString().CompareTo(b.Last().ToString()); });
        fromExit.Sort((a, b) => { return a.Last().ToString().CompareTo(b.Last().ToString()); });

        if (startExit.Count() == 0) // если нет пути до выхода.
            return new MoveDirection[0];

        //Console.WriteLine("fromStart" + fromStart.Count());
        if (fromStart.Count == 0) // если нет сундуков.
        {
            var pathToList = startExit.First().ToList();
            return pathToMoveArray(pathToList);
        }

        int best = int.MaxValue;
        int index = -1;

        // ну да... цикл...
        // ищем, какой сундук выгоднее всего собрать.
        for (int i = 0; i < fromStart.Count; i++)
        {
            if (fromStart[i].Length + fromExit[i].Length < best)
            {
                best = fromStart[i].Length + fromExit[i].Length;
                index = i;
            }
        }

        // массив движений персонажа.
        var ans = new MoveDirection[best - 2];
        // сначала от персонажа до сундука.
        var startToList = fromStart[index].ToList();
        startToList.Reverse();
        pathToMoveArray(startToList).CopyTo(ans, 0);

        // потом от сундука до выхода.
        var exitToList = fromExit[index].ToList();
        pathToMoveArray(exitToList).CopyTo(ans, fromStart[index].Length - 1);
        return ans;
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using Greedy.Architecture;
using Microsoft.CodeAnalysis;

namespace Greedy;

public class GreedyPathFinder : IPathFinder
{
    public List<Point> FindPathToCompleteGoal(State state)
    {
        // вытаскиваем все нужные значения.
        var goal = state.Goal;
        var currentPoint = state.Position;
        var currentEnergy = state.Energy;
        var chestList = new List<Point>(state.Chests);
        //Console.WriteLine(goal);
        var result = new List<Point>();
        var pathFinder = new DijkstraPathFinder();

        // пустой список, если нам подсунули пустой лабиринт или ничего не просят.
        if (state.Goal == 0 || state.Chests.Count < state.Goal)
            return new List<Point>();

        // делаем, пока не выполним план по сундукам.
        while (goal > 0)
        {
            // пути будем находить с помощью алгоритма Дейкстры.
            var paths = pathFinder.GetPathsByDijkstra(state, currentPoint, chestList);

            // путь до сундука вообще существует?
            if (paths.Any())
            {
                currentEnergy = currentEnergy - paths.First().Cost;

                // возвращаем пустой список, если мы не можем идти дальше.
                if (currentEnergy < 0)
                    return new List<Point>();

                // записываем ответ, пропуская стартовую точку.
                result.AddRange(paths.First().Path.Skip(1));
                currentPoint = paths.First().Path.Last();
                chestList.Remove(paths.First().Path.Last());
            }
            else // пустой список, если нет пути до сундука.
                return new List<Point>();
            
            goal = goal - 1; // приближаемся к плановому количеству сундуков.
        }

        return result;
    }
}

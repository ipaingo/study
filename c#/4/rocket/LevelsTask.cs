using System;
using System.Collections.Generic;

namespace func_rocket;

public class LevelsTask
{
	static readonly Physics standardPhysics = new();

	public static IEnumerable<Level> CreateLevels()
	{
		yield return new Level("Zero", 
			new Rocket(new Vector(200, 500), Vector.Zero, -0.5 * Math.PI),
			new Vector(600, 200), 
			(size, v) => Vector.Zero, standardPhysics);

        yield return new Level("Heavy",
            new Rocket(new Vector(200, 500), Vector.Zero, -0.5 * Math.PI),
            new Vector(600, 200),
            (size, v) => new Vector(0, 0.9), standardPhysics);

        yield return new Level("Up", 
			new Rocket(new Vector(200, 500), Vector.Zero, -0.5 * Math.PI),
			new Vector(700, 500),
            // с плюсом - вниз, с минусом - вверх.
            (size, v) => new Vector(0, -(300 / (size.Y - v.Y + 300))), standardPhysics);

        yield return new Level("WhiteHole",
            new Rocket(new Vector(200, 500), Vector.Zero, -0.5 * Math.PI),
            new Vector(600, 200),
            (size, v) =>
            {
                // вектор от игрока к дырке.
                Vector direction = (new Vector(600, 200) - v);
                // делаем его единичным по длине, потому что нам нужно направление.
                Vector normal = direction.Normalize();

                var d = direction.Length;
                // считаем по формуле.
                return new Vector(-normal.X * (140 * d / (d * d + 1)), -normal.Y * (140 * d / (d * d + 1)));
            }, standardPhysics);

        yield return new Level("BlackHole",
            new Rocket(new Vector(200, 500), Vector.Zero, -0.5 * Math.PI),
            new Vector(600, 200),
            (size, v) =>
            {
                // вектор от игрока к середине между игроком и дыркой.
                Vector direction = (new Vector((600 + 200) / 2, (200 + 500) / 2) - v);
                Vector normal = direction.Normalize();

                var d = direction.Length;
                // аналогично, но в другую сторону и с немного другими числами.
                return new Vector(normal.X * (300 * d / (d * d + 1)), normal.Y * (300 * d / (d * d + 1)));
            }, standardPhysics);

        yield return new Level("BlackAndWhite",
            new Rocket(new Vector(200, 500), Vector.Zero, -0.5 * Math.PI),
            new Vector(600, 200),
            (size, v) =>
            {
                // белая.
                Vector direction1 = (new Vector(600, 200) - v);
                Vector normal1 = direction1.Normalize();
                // черная.
                Vector direction2 = (new Vector((600 + 200) / 2, (200 + 500) / 2) - v);
                Vector normal2 = direction2.Normalize();

                var d1 = direction1.Length;
                var d2 = direction2.Length;
                // среднее арифметическое.
                return (new Vector(-normal1.X * (140 * d1 / (d1 * d1 + 1)), -normal1.Y * (140 * d1 / (d1 * d1 + 1)))
                + new Vector(normal2.X * (300 * d2 / (d2 * d2 + 1)), normal2.Y * (300 * d2 / (d2 * d2 + 1)))) / 2;
            }, standardPhysics);
    }
}
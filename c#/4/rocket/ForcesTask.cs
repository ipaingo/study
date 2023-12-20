using System;

namespace func_rocket;

public class ForcesTask
{
    /// <summary>
    /// Создает делегат, возвращающий по ракете вектор силы тяги двигателей этой ракеты.
    /// Сила тяги направлена вдоль ракеты и равна по модулю forceValue.
	/// 
    /// координаты: x = F * cos, y = F * sin.
    /// </summary>
    public static RocketForce GetThrustForce(double forceValue) => r => new Vector(forceValue * Math.Cos(r.Direction), forceValue * Math.Sin(r.Direction));

    /// <summary>
    /// Преобразует делегат силы гравитации, в делегат силы, действующей на ракету.
    /// </summary>
    public static RocketForce ConvertGravityToForce(Gravity gravity, Vector spaceSize) => r => gravity(spaceSize, r.Location);

    /// <summary>
    /// Суммирует все переданные силы, действующие на ракету, и возвращает суммарную силу.
    /// </summary>
    public static RocketForce Sum(params RocketForce[] forces) => rocket =>
    {
        Vector vec = new Vector(0, 0);

        foreach (var forcesItem in forces)
            vec += forcesItem(rocket);

        return vec;
    };

    // управлять им сложнее, чем кажется.
}
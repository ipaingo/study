using Inheritance.Geometry.Visitor;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Inheritance.Geometry.Virtual
{
    public abstract class Body
    {
        public Vector3 Position { get; }
        protected Body(Vector3 position)
        {
            Position = position;
        }
        public abstract bool ContainsPoint(Vector3 point);
        public abstract RectangularCuboid GetBoundingBox();
    }
    // теперь информация об объектах определена в соответствующих классах вместо кучи ифов.
    // для каждого вместе соединены старые классы геометрических тел и части ContainsPoint,
    // а также реализован GetBoundingBox.
    public class Ball : Body
    {
        public double Radius { get; }
        public Ball(Vector3 position, double radius) : base(position)
        {
            Radius = radius;
        }
        public override bool ContainsPoint(Vector3 point)
        {
            var vector = point - Position;
            var length2 = vector.GetLength2();
            return length2 <= Radius * Radius;
        }
        public override RectangularCuboid GetBoundingBox()
        {
            // есть куб размером диаметр на диаметр на диаметр.
            return new RectangularCuboid(Position, 2 * Radius, 2 * Radius, 2 * Radius);
        }
    }

    public class RectangularCuboid : Body
    {
        public double SizeX { get; }
        public double SizeY { get; }
        public double SizeZ { get; }
        public RectangularCuboid(Vector3 position, double sizeX, double sizeY, double sizeZ) : base(position)
        {
            SizeX = sizeX;
            SizeY = sizeY;
            SizeZ = sizeZ;
        }
        public override bool ContainsPoint(Vector3 point)
        {
            var minPoint = new Vector3(
                Position.X - SizeX / 2,
                Position.Y - SizeY / 2,
                Position.Z - SizeZ / 2);
            var maxPoint = new Vector3(
                Position.X + SizeX / 2,
                Position.Y + SizeY / 2,
                Position.Z + SizeZ / 2);

            return point >= minPoint && point <= maxPoint;
        }
        public override RectangularCuboid GetBoundingBox()
        {
            // для параллелепипеда граница это он сам.
            return new RectangularCuboid(Position, SizeX, SizeY, SizeZ);
        }
    }

    public class Cylinder : Body
    {
        public double SizeZ { get; }
        public double Radius { get; }
        public Cylinder(Vector3 position, double sizeZ, double radius) : base(position)
        {
            SizeZ = sizeZ;
            Radius = radius;
        }
        public override bool ContainsPoint(Vector3 point)
        {
            var vectorX = point.X - Position.X;
            var vectorY = point.Y - Position.Y;
            var length2 = vectorX * vectorX + vectorY * vectorY;
            var minZ = Position.Z - SizeZ / 2;
            var maxZ = minZ + SizeZ;

            return length2 <= Radius * Radius && point.Z >= minZ && point.Z <= maxZ;
        }

        public override RectangularCuboid GetBoundingBox()
        {
            // в высоту просто высота, оставшиеся размеры - диаметр.
            return new RectangularCuboid(Position, 2 * Radius, 2 * Radius, SizeZ);
        }
    }

    public class CompoundBody : Body
    {
        public IReadOnlyList<Body> Parts { get; }
        public CompoundBody(IReadOnlyList<Body> parts) : base(parts[0].Position)
        {
            Parts = parts;
        }
        public override bool ContainsPoint(Vector3 point)
        {
            return Parts.Any(body => body.ContainsPoint(point));
        }
        public override RectangularCuboid GetBoundingBox()
        {
            // сделаем параллелепипед по двум точкам:
            // самой "правой верхней дальней" и самой "левой нижней ближней".
            // для этого возьмем максимальную/минимальную координату "коробки" из всех составляющих,
            // а для этого нужно отсчитать половину размера коробки от центра коробки
            // в большую сторону для максимальных и в меньшую для минимальных.
            var maxX = Parts.Max(body => body.GetBoundingBox().Position.X + body.GetBoundingBox().SizeX / 2);
            var maxY = Parts.Max(body => body.GetBoundingBox().Position.Y + body.GetBoundingBox().SizeY / 2);
            var maxZ = Parts.Max(body => body.GetBoundingBox().Position.Z + body.GetBoundingBox().SizeZ / 2);

            var minX = Parts.Min(body => body.GetBoundingBox().Position.X - body.GetBoundingBox().SizeX / 2);
            var minY = Parts.Min(body => body.GetBoundingBox().Position.Y - body.GetBoundingBox().SizeY / 2);
            var minZ = Parts.Min(body => body.GetBoundingBox().Position.Z - body.GetBoundingBox().SizeZ / 2);

            return new RectangularCuboid(
                new Vector3((maxX + minX) / 2, (maxY + minY) / 2, (maxZ + minZ) / 2),
                maxX - minX, maxY - minY, maxZ - minZ);
        }
    }
}
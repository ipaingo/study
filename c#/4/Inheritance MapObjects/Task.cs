using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Inheritance.MapObjects
{
    public interface IOwnable
    {
        int Owner { get; set; }
    }

    public interface IFightable
    {
        Army Army { get; set; }
    }

    public interface IConsumable
    {
        Treasure Treasure { get; set; }
    }

    public class Dwelling : IOwnable
    {
        public int Owner { get; set; }
    }

    public class Mine : IOwnable, IFightable, IConsumable
    {
        public int Owner { get; set; }
        public Army Army { get; set; }
        public Treasure Treasure { get; set; }
    }

    public class Creeps : IFightable, IConsumable
    {
        public Army Army { get; set; }
        public Treasure Treasure { get; set; }
    }

    public class Wolves : IFightable
    {
        public Army Army { get; set; }
    }

    public class ResourcePile : IConsumable
    {
        public Treasure Treasure { get; set; }
    }

    public static class Interaction
    {
        public static void Make(Player player, object mapObject)
        {
            // вместо прописанных интеракций теперь только то,
            // что надо делать с объектами.

            // порядок не случаен. сначала проверяем, победил ли игрок.
            if (mapObject is IFightable fightObject)
            {
                if (!player.CanBeat(fightObject.Army))
                {
                    player.Die();
                    return;
                }
            }
            // только затем проверяем, забирает ли он себе награду.
            if (mapObject is IOwnable ownObject)
            {
                ownObject.Owner = player.Id;
            }

            if (mapObject is IConsumable consumeObject)
            {
                player.Consume(consumeObject.Treasure);
            }
        }
    }
}

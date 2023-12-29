using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;
using System.Reflection;

namespace Reflection.Randomness
{
    public class FromDistribution : Attribute
    {
        // реализуем интерфейсик (ну, он 4 строчки занимает, это как-то мило).
        public IContinuousDistribution Distribution { get; }

        public FromDistribution(Type type, params object[] args)
        {
            try
            {
                // пробуем создать экземпляр.
                Distribution = (IContinuousDistribution)Activator.CreateInstance(type, args);
            }
            catch
            {
                // информативное сообщение при ошибке.
                throw new ArgumentException("failed to create " + type.FullName + ".");
            }
        }
    }

    class Generator<T> where T : new()
    {
        Dictionary<PropertyInfo, FromDistribution> dict = new Dictionary<PropertyInfo, FromDistribution>();

        // при создании генератору мы передаем тип класса и его поля.
        // таким образом, свойства будут использоваться при генерации нового класса.
        public Generator()
        {
            foreach (var property in typeof(T).GetProperties().Where(p => p.GetCustomAttribute<FromDistribution>() != null))
            {
                dict.Add(property, property.GetCustomAttribute<FromDistribution>());
            }
        }

        public T Generate(Random rand)
        {
            var result = new T();
            foreach (var item in dict)
            {
                item.Key.SetValue(result, item.Value.Distribution.Generate(rand));
            }

            return result;
        }
    }
}

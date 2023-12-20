using Generics.BinaryTrees;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Generics.BinaryTrees
{
    // с днем алгоритмического программирования!
    public class BinaryTree<T> : IEnumerable<T> where T : IComparable
    {
        public BinaryTree<T> Left { get; private set; }
        public BinaryTree<T> Right { get; private set; }
        public T Value { get; private set; }
        public bool Exists = false;

        public void Add(T value)
        {
            if (!Exists)
            {
                Exists = true;
                Value = value;
            }
            else
            {
                var current = this;     // чтобы добавить в дерево элемент,
                while (current != null) // нам нужно сравнивать этот элемент с уже имеющимися узлами,
                {                       // пока мы не найдем для него место.
                    if (current.Value.CompareTo(value) >= 0)
                    {
                        if (current.Left == null)
                        {
                            current.Left = new BinaryTree<T> { value };
                            break;
                        }
                        else
                            current = current.Left;
                    }
                    else
                    {
                        if (current.Right == null)
                        {
                            current.Right = new BinaryTree<T> { value };
                            break;
                        }
                        else
                            current = current.Right;
                    }
                }
            }
        }

        // так как я не стала хранить все дерево в виде
        // какой-нибудь коллекции, например, которую можно просто взять и вернуть,
        // потребовалось реализовать GetEnumerator.
        // осталось понять, что хуже, лишняя память или лишний цикл?
        public IEnumerator<T> GetEnumerator()
        {
            // но никто не пришел.
            if (!Exists)
                yield break;
            // сначала проходим по левой ветке,
            if (Left != null)
            {
                var left = Left.GetEnumerator();
                while (left.MoveNext())
                    yield return left.Current;
            }
            // затем само значение,
            yield return Value;
            // затем правая ветка.
            if (Right != null)
            {
                var right = Right.GetEnumerator();
                while (right.MoveNext())
                    yield return right.Current;
            }
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
    }

    public static class BinaryTree
    {
        public static BinaryTree<T> Create<T>(params T[] values) where T : IComparable
        {
            var binTree = new BinaryTree<T>();
            foreach (var value in values)
                binTree.Add(value);

            return binTree;
        }
    }
}

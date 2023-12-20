using NUnit.Framework.Constraints;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Xml.Linq;

namespace BinaryTrees;
public class BinaryTree<T> : IEnumerable<T> where T : IComparable
{
    public T Value { get; set; }
    public BinaryTree<T> LeftSon { get; set; }
    public BinaryTree<T> RightSon { get; set; }
    public int Length { get; set; }
    public BinaryTree() { }
    public BinaryTree(T value)
    {
        Value = value;
        LeftSon = null;
        RightSon = null;
        Length = 1;
    }

    private BinaryTree<T> init;

    public void Add(T value)
    {
        if (init == null)
        {
            init = new BinaryTree<T>(value);
            return;
        }

        BinaryTree<T> current = init;

        while (current != null)
        {
            current.Length++;
            if (current.Value.CompareTo(value) < 0)
            {
                if (current.LeftSon != null)
                    current = current.LeftSon;
                else
                {
                    current.LeftSon = new BinaryTree<T>(value);
                    return;
                }
            }
            else
            {
                if (current.RightSon != null)
                    current = current.RightSon;
                else
                {
                    current.RightSon = new BinaryTree<T>(value);
                    return;
                }
            }
        }
    }

    public bool Contains(T key)
    {
        BinaryTree<T> current = init;
        while (current != null)
        {
            int compareResult = key.CompareTo(current.Value);

            if (compareResult == 0)
                return true;
            else if (compareResult > 0)
                current = current.LeftSon;
            else
                current = current.RightSon;
        }

        return false;
    }

    public IEnumerator<T> GetEnumerator() => GetEnumerator(init);
    private IEnumerator<T> GetEnumerator(BinaryTree<T> Node)
    {
        if (Node == null)
            yield break;

        var right = GetEnumerator(Node.RightSon);
        while (right.MoveNext())
            yield return right.Current;

        yield return Node.Value;

        var left = GetEnumerator(Node.LeftSon);
        while (left.MoveNext())
            yield return left.Current;
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public T this[int i]
    {
        get
        {
            var current = init;
            int currentLength = 0;
            int currentIndex;

            while (true)
            {
                if (current.RightSon == null)
                    currentIndex = currentLength;
                else
                    currentIndex = current.RightSon.Length + currentLength;

                if (i == currentIndex)
                    return current.Value;
                if (i < currentIndex)
                    current = current.RightSon;
                else
                {
                    current = current.LeftSon;
                    currentLength = currentIndex + 1;
                }
            }
        }
    }
}

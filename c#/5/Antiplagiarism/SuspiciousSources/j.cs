using NUnit.Framework.Constraints;
using System;
using System.Collections;
using System.Collections.Generic;
using System.Xml.Linq;

namespace BinaryTrees;

public class BinaryTree<T> : IEnumerable<T> where T : IComparable {
    public class Node {
        public T value;
        public Node left = null;
        public Node right = null;
        public int len = 1;
    }

    Node root = null;

    public void Add(T node) {
        if (root == null) {
            root = new Node();
            root.value = node;
            return;
        }

        var cur = root;
        while (cur != null) {
            cur.len++;
            if (cur.value.CompareTo(node) < 0) {
                if (cur.left != null) {
                    cur = cur.left;
                } else {
                    cur.left = new Node();
                    cur.left.value = node;
                    break;
                }
            } else {
                if (cur.right != null) {
                    cur = cur.right;
                } else {
                    cur.right = new Node();
                    cur.right.value = node;
                    break;
                }
            }
        }
    }

    public bool Contains(T key) {
        var cur = root;
        while (cur != null) {
            if (cur.value.Equals(key)) 
                return true;

            cur = (cur.value.CompareTo(key) < 0 ? cur.left : cur.right);
        }
        return false;
    }

    public IEnumerator<T> GetEnumerator() => GetEnumerator(root);
    private IEnumerator<T> GetEnumerator(Node cur)
    {
        if (cur == null)
            yield break;

        var r = GetEnumerator(cur.right);
        while (r.MoveNext())
            yield return r.Current;

        yield return cur.value;

        var l = GetEnumerator(cur.left);
        while (l.MoveNext())
            yield return l.Current;
    }
    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public T this[int i]
    {
        get
        {
            var cur = root;
            int cur_len = 0;
            while (true)
            {
                int cur_index = (cur.right == null ? 0 : cur.right.len) + cur_len;
                if (i == cur_index)
                    return cur.value;
                if (i < cur_index)
                    cur = cur.right;
                else
                {
                    cur = cur.left;
                    cur_len = cur_index + 1;
                }
            }
        }
    }
}
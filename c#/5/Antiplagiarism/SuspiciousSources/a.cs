using System;
using System.Collections;
using System.Collections.Generic;

namespace BinaryTrees
{
    public class BinaryTree<T> : IEnumerable<T> where T : IComparable
    {
        private T valueNode;               // Значение текущего узла
        private BinaryTree<T> leftSon;     // Левый потомок текущего узла
        private BinaryTree<T> rightSon;    // Правый потомок текущего узла
        private bool initialized = false;  // Флаг инициализации дерева

        int weight = 1;                    // Номер элемента

        public BinaryTree() { }
        public BinaryTree(T value)
        {
            valueNode = value;
            initialized = true;
        }

        // Добавление нового элемента с ключом key в дерево
        public void Add(T key)
        {
            if (!initialized)
            {
                valueNode = key;    // Если дерево не инициализировано, создаем корневой узел
                initialized = true;
                return;
            }

            BinaryTree<T> parentNode = this;
            // Поиск места для вставки
            while (true)
            {
                parentNode.weight++;            // Увеличение номера элемента

                int compare = parentNode.valueNode.CompareTo(key);
                if (compare > 0)
                {
                    if (parentNode.leftSon != null)
                        parentNode = parentNode.leftSon;
                    else
                    {
                        parentNode.leftSon = new BinaryTree<T>(key);  // Вставляем слева
                        break;
                    }
                }
                else
                {
                    if (parentNode.rightSon != null)
                        parentNode = parentNode.rightSon;
                    else
                    {
                        parentNode.rightSon = new BinaryTree<T>(key);  // Вставляем справа
                        break;
                    }
                }
            }
        }

        // Метод для проверки наличия элемента с ключом key в дереве
        public bool Contains(T key)
        {
            if (!initialized)
                return false;  // Если дерево пустое, элемент не найден

            BinaryTree<T> parentNode = this;
            while (true)
            {
                int compareResult = parentNode.valueNode.CompareTo(key);
                // Элемент найден
                if (compareResult == 0)
                    return true;

                if (compareResult > 0)
                {
                    if (parentNode.leftSon != null)
                        parentNode = parentNode.leftSon;
                    else
                        return false;  // Элемент не найден в левом поддереве
                }
                else
                {
                    if (parentNode.rightSon != null)
                        parentNode = parentNode.rightSon;
                    else
                        return false;  // Элемент не найден в правом поддереве
                }
            }
        }

        public IEnumerator<T> GetEnumerator() => EnumeratorNode(this);

        /// <summary>
        /// Рекурсивный обход бинарного дерева
        /// </summary>
        /// <param name="root">Корень</param>
        /// <returns></returns>
        IEnumerator<T> EnumeratorNode(BinaryTree<T> root)
        {
            // Не инициализирован
            if (root == null || !root.initialized)
                yield break;
            // Рекурсивный вызова левого потомка
            var enumeratorTreeNode = EnumeratorNode(root.leftSon);

            while (enumeratorTreeNode.MoveNext())
                yield return enumeratorTreeNode.Current;
            yield return root.valueNode;
            // Рекурсивный вызов правого потомка
            enumeratorTreeNode = EnumeratorNode(root.rightSon);
            
            while (enumeratorTreeNode.MoveNext())
                yield return enumeratorTreeNode.Current;
        }

        IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

        /// <summary>
        /// Получение элементов по индексу
        /// </summary>
        /// <param name="i">Индекс</param>
        /// <returns></returns>
        public T this[int i]
        {
            get
            {
                BinaryTree<T> current = this;       // Корневой узел
                int parentWeight = 0;               // Вес родительского узла = 0

                while (true)
                {
                    // Индекс текущего узла относительно его родительского узла
                    int currentNodeIndex = 0;
                    if (current.leftSon == null)
                        currentNodeIndex = 0;
                    else  
                        currentNodeIndex = current.leftSon.weight; 
                    currentNodeIndex += parentWeight;

                    if (i == currentNodeIndex)
                        return current.valueNode;   // Вернуть значение текущего узла, если индекс совпадает

                    // Перемещаемся в левое поддерево, если индекс меньше текущего индекса
                    if (i < currentNodeIndex)
                        current = current.leftSon;
                    else
                    {
                        // Перемещаемся в правое поддерево, обновляем вес родительского узла
                        current = current.rightSon;
                        parentWeight = currentNodeIndex + 1;
                    }
                }
            }
        }

    }
}

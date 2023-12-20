using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Generics.Tables
{
    public class Table<TRow, TColumn, TValue>
    {
        public Dictionary<TRow, Dictionary<TColumn, TValue>> values = new Dictionary<TRow, Dictionary<TColumn, TValue>>();
        public HashSet<TRow> Rows = new HashSet<TRow>();
        public HashSet<TColumn> Columns = new HashSet<TColumn>();

        public Indexator<TRow, TColumn, TValue> Open
        {
            get
            {
                return new Indexator<TRow, TColumn, TValue>(this, true);
            }
        }
        public Indexator<TRow, TColumn, TValue> Existed
        {
            get
            {
                return new Indexator<TRow, TColumn, TValue>(this, false);
            }
        }

        public void AddRow(TRow row)
        {
            Rows.Add(row);
        }

        public void AddColumn(TColumn col)
        {
            Columns.Add(col);
        }
    }

    public class Indexator<TRow, TColumn, TValue>
    {
        private Table<TRow, TColumn, TValue> Table;
        private bool Changeable;

        public Indexator(Table<TRow, TColumn, TValue> table, bool changeable)
        {
            Table = table;
            Changeable = changeable;
        }

        public TValue this[TRow i, TColumn j]
        {
            get
            {
                if (!Table.Rows.Contains(i) || !Table.Columns.Contains(j))
                {
                    if (Changeable)
                        return default(TValue);
                    else
                        throw new ArgumentException();
                }

                if (!Table.values.ContainsKey(i) || !Table.values[i].ContainsKey(j))
                    return default(TValue);

                return Table.values[i][j];
            }

            set
            {
                if (!Table.Rows.Contains(i))
                {
                    if (!Changeable)
                        throw new ArgumentException();

                    Table.Rows.Add(i);

                }

                if (!Table.Columns.Contains(j))
                {
                    if (!Changeable)
                        throw new ArgumentException();

                    Table.Columns.Add(j);
                }

                if (!Table.values.ContainsKey(i))
                    Table.values[i] = new Dictionary<TColumn, TValue>();

                Table.values[i][j] = value;
            }
        }
    }
}

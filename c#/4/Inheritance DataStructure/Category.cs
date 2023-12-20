using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace Inheritance.DataStructure
{
    public class Category : IComparable
    {
        public string CategoryName { get; set; }
        public MessageType MessageType { get; set; }
        public MessageTopic MessageTopic { get; set; }
        public Category(string name, MessageType messageType, MessageTopic messageTopic)
        {
            CategoryName = name;
            MessageType = messageType;
            MessageTopic = messageTopic;
        }


        public bool Equals(Category obj)
        {
            // можно было и в один ретерн написать, но так легче читается.
            if (obj is null) return false;
            if (CategoryName != obj.CategoryName) return false;
            if (MessageType != obj.MessageType) return false;
            if (MessageTopic != obj.MessageTopic) return false;
            return true;
        }

        public override int GetHashCode()
        {
            // счастливые числа - должно везти с коллизиями. ;)
            return CategoryName.GetHashCode() * 357 + MessageType.GetHashCode() * 573 + MessageTopic.GetHashCode() * 735;
        }


        public int CompareTo(object obj) // реализует интерфейс IComparable.
        {
            if (!(obj is Category)) // жалко, что is not добавили только в 9.0.
                return -1;
            // проверим, что сравниваемый объект - тоже категория, и что он не пуст.
            if (obj is null)
                return -1;

            var objCategory = obj as Category;
            // теперь сравним объекты.
            return (CategoryName, MessageType, MessageTopic).CompareTo((objCategory.CategoryName, objCategory.MessageType, objCategory.MessageTopic));
        }


        // перегрузка операторов с помощью интерфейса.
        public static bool operator <=(Category a, Category b)
        {
            if (a.CompareTo(b) <= 0) return true;
            return false;
        }
        public static bool operator >=(Category a, Category b)
        {
            if (a.CompareTo(b) >= 0) return true;
            return false;
        }

        public static bool operator <(Category a, Category b)
        {
            if (a.CompareTo(b) < 0) return true;
            return false;
        }
        public static bool operator >(Category a, Category b)
        {
            if (a.CompareTo(b) > 0) return true;
            return false;
        }

        public static bool operator ==(Category a, Category b)
        {
            if (a.CompareTo(b) == 0) return true;
            return false;
        }
        public static bool operator !=(Category a, Category b)
        {
            if (a.CompareTo(b) != 0) return true;
            return false;
        }

        // в тестах также просят перегрузить tostring.
        public override string ToString()
        {
            var ans = CategoryName + "." + MessageType.ToString() + "." + MessageTopic.ToString();
            return ans;
        }
    }
}

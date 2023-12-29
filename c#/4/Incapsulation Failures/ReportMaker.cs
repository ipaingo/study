using NUnit.Framework.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Incapsulation.Failures
{
    // лучше, чем просто цифры и саммари с объяснениями.
    public enum FailureType
    {
        UnexpectedShutdown,
        ShortNonResponding,
        HardwareFailure,
        ConnectionProblem
    }

    public class Device
    {
        public int Id;
        public string Name;
        public Failure Failure;

        public Device(int id, string name, Failure failure)
        {
            this.Id = id;
            this.Name = name;
            this.Failure = failure;
        }
    }

    public class Failure
    {
        public FailureType Type;
        public DateTime Date;

        public Failure(FailureType type, DateTime date)
        {
            this.Type = type;
            this.Date = date;
        }

        // это поле теперь здесь, что вполне логично.
        public bool IsFailureSerious()
        {
            return this.Type == FailureType.UnexpectedShutdown || this.Type == FailureType.HardwareFailure;
        }
    }

    public class Common
    {
        // вот это вообще жесть была, конечно.
        public static bool IsDateEarlier(DateTime date1, DateTime date2)
        {
            return date1 < date2;
        }
    }

    public class ReportMaker
    {
        public static List<string> FindDevicesFailedBeforeDateObsolete(
            int day,
            int month,
            int year,
            int[] failureTypes,
            int[] deviceId,
            object[][] times,
            List<Dictionary<string, object>> devices)
        {
            var devicesList = new Device[deviceId.Length]; // список устройств.

            for (int i = 0; i < deviceId.Length; i++)
            {
                // для удобства и читаемости отдельно соберем дату и типы ошибок.
                var failDate = new DateTime((int)times[i][2], (int)times[i][1], (int)times[i][0]);
                var fail = new Failure((FailureType)failureTypes[i], failDate);
                devicesList[i] = new Device((int)devices[i]["DeviceId"], (string)devices[i]["Name"], fail);
            }

            var date = new DateTime(year, month, day);
            return FindDevicesFailedBeforeDate(date, devicesList);
        }

        public static List<string> FindDevicesFailedBeforeDate(DateTime date, Device[] deviceList)
        {
            // соберем айдишники всех подходящих случаев в массив.
            var problematicDevices = new HashSet<int>();
            for (int i = 0; i < deviceList.Length; i++)
                if (deviceList[i].Failure.IsFailureSerious() && Common.IsDateEarlier(deviceList[i].Failure.Date, date))
                    problematicDevices.Add(deviceList[i].Id);

            // вернем список имен устройств, которые подходят под условие.
            return deviceList
                .Where(device => problematicDevices.Contains(device.Id))
                .Select(device => device.Name)
                .ToList();
        }
    }
}

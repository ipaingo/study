using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Incapsulation.Failures
{

    public enum Failure
    {
        UnexpectedShutdown,
        ShortNonResponding,
        HardwareFailure,
        ConnectionProblem
    }

    public class Device
    {
        public int id;
        public string name;

        public Device(int deviceId, string deviceName)
        {
            this.id = deviceId;
            this.name = deviceName;
        }
    }

    public class Common
    {
        public static bool IsFailureSerious(Failure failureType)
        {
            return failureType == Failure.UnexpectedShutdown || failureType == Failure.HardwareFailure;
        }


        public static bool Earlier(DateTime date1, DateTime date2)
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

            var problematicDevices = new HashSet<int>();

            for (int i = 0; i < failureTypes.Length; i++)
            {
                var date = new DateTime((int)times[i][2], (int)times[i][1], (int)times[i][0]);
                if (Common.IsFailureSerious((Failure)failureTypes[i]) && Common.Earlier(date, new DateTime(year, month, day)))
                    problematicDevices.Add(deviceId[i]);
            }

            var devicesList = devices
                .Select(device => new Device((int)device["DeviceId"], device["Name"] as string))
                .ToList();

            return FindDevicesFailedBeforeDate(problematicDevices, devicesList, new DateTime(year, month, day));
        }

        public static List<string> FindDevicesFailedBeforeDate(HashSet<int> problematicDevices, List<Device> devices, DateTime uselessDateTime)
        {
            return devices
                .Where(device => problematicDevices.Contains(device.id))
                .Select(device => device.name)
                .ToList();
        }


    }
}

namespace func_rocket;

//public class ControlTask
//{
//    public static Turn ControlRocket(Rocket rocket, Vector target)
//    {
//        var direction = target - rocket.Location;
//        if (direction.Angle - (rocket.Direction * 3 + rocket.Velocity.Angle * 7) / 10 > 0)
//            return Turn.Right;

//        return Turn.Left;
//    }
//}

public class ControlTask
{
	public static Turn ControlRocket(Rocket rocket, Vector target)
	{
		return Turn.None;
	}
}

//(rocket.Direction + rocket.Velocity.Angle* 3) / 4

using NUnit.Framework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;

namespace Documentation;

public class Specifier<T> : ISpecifier
{
    public string GetApiDescription()
    {
        // ����� ���������. ������ ��������.
        // � ���� ���� ������� ���������� null ��� �������� ��������� � ������� ?.
        return typeof(T).GetCustomAttribute<ApiDescriptionAttribute>()?.Description;
    }

    public string[] GetApiMethodNames()
    {
        return typeof(T).GetMethods() // �������, ������-�, ������.
            .Where(methodType => methodType.GetCustomAttribute<ApiMethodAttribute>() != null) // � ������� ���� �������.
            .Where(methodType => methodType.IsPublic) // � ����� public.
            .Select(methodType => methodType.Name) // � ����� ��� �����.
            .ToArray();
    }

    public string GetApiMethodDescription(string methodName)
    {
        // ��� GetApiDescription, �� ��� ������.
        return typeof(T).GetMethod(methodName)?.GetCustomAttribute<ApiDescriptionAttribute>()?.Description;
    }

    public string[] GetApiMethodParamNames(string methodName)
    {
        return typeof(T).GetMethod(methodName)?.GetParameters() // ������� ��������� ������,
            .Select(param => param.Name) // ������� �����.
            .ToArray();
    }

    public string GetApiMethodParamDescription(string methodName, string paramName)
    {
        var methodType = typeof(T).GetMethod(methodName); // ��� �����.
        if (methodType == null)
            return null; // ������ ����, ���� ������ ���.

        var paramType = methodType?.GetParameters() // ����� ��� ���������.
            .Where(param => param.Name == paramName) // ��� ����� ����������,
            .Where(param => param.GetCustomAttribute<ApiDescriptionAttribute>() != null); // � ����� � �������� ���-�� ����.

        if (paramType.Count() == 0) return null;
        return paramType
            .First()
            .GetCustomAttribute<ApiDescriptionAttribute>()
            .Description;
    }

    // ��������������� �����. ���������� �������� ���������.
    public ApiParamDescription GetApiParamDescription(ParameterInfo paramInfo)
    {
        if (paramInfo == null)
            return null;

        var desc = new ApiParamDescription();

        if (paramInfo.Name != string.Empty)
            desc.ParamDescription = new CommonDescription(paramInfo.Name, paramInfo.GetCustomAttribute<ApiDescriptionAttribute>()?.Description);
        else
            desc.ParamDescription = new CommonDescription(null, paramInfo.GetCustomAttribute<ApiDescriptionAttribute>()?.Description);

        if (paramInfo.GetCustomAttribute<ApiRequiredAttribute>()?.Required == null)
            desc.Required = false;
        else
            desc.Required = (bool)(paramInfo.GetCustomAttribute<ApiRequiredAttribute>()?.Required);

        desc.MinValue = paramInfo.GetCustomAttribute<ApiIntValidationAttribute>()?.MinValue;
        desc.MaxValue = paramInfo.GetCustomAttribute<ApiIntValidationAttribute>()?.MaxValue;

        return desc;
    }

    public ApiParamDescription GetApiMethodParamFullDescription(string methodName, string paramName)
    {
        var methodType = typeof(T).GetMethod(methodName);
        if (methodType == null)
            // ������ ��������.
            return new ApiParamDescription() { ParamDescription = new CommonDescription(paramName) };

        ParameterInfo param = null;
        foreach (var p in methodType?.GetParameters())
            if (p.Name == paramName)
                param = p; // ����������� ������ ��������.

        if (param == null)
            // ������ ��������.
            return new ApiParamDescription() { ParamDescription = new CommonDescription(paramName) };

        // ����� ����������� �������� � ����������.
        return GetApiParamDescription(param);
    }

    public ApiMethodDescription GetApiMethodFullDescription(string methodName)
    {
        var methodType = typeof(T).GetMethod(methodName);
        // ������ ���������� ����, ���� �����.
        if (methodType == null)
            return null;
        if (methodType.GetCustomAttribute<ApiMethodAttribute>() == null)
            return null;

        // �������� ���������.
        var result = new ApiMethodDescription();
        result.MethodDescription = new CommonDescription(methodName, GetApiMethodDescription(methodName));
        if (methodType.ReturnType != typeof(void))
            result.ReturnDescription = GetApiParamDescription(methodType.ReturnParameter);

        // �������� ����������.
        var list = new List<ApiParamDescription>();
        foreach (var param in methodType.GetParameters())
        {
            if (GetApiParamDescription(param) != null)
                list.Add(GetApiParamDescription(param));
        }

        result.ParamDescriptions = list.ToArray();

        return result;
    }
}
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
        // очень буквально. просто описания.
        // в этом коде массово возвращаем null без бросания исключний с помощью ?.
        return typeof(T).GetCustomAttribute<ApiDescriptionAttribute>()?.Description;
    }

    public string[] GetApiMethodNames()
    {
        return typeof(T).GetMethods() // получим, значит-с, методы.
            .Where(methodType => methodType.GetCustomAttribute<ApiMethodAttribute>() != null) // у которых есть атрибут.
            .Where(methodType => methodType.IsPublic) // и чтобы public.
            .Select(methodType => methodType.Name) // и нужны нам имена.
            .ToArray();
    }

    public string GetApiMethodDescription(string methodName)
    {
        // как GetApiDescription, но для метода.
        return typeof(T).GetMethod(methodName)?.GetCustomAttribute<ApiDescriptionAttribute>()?.Description;
    }

    public string[] GetApiMethodParamNames(string methodName)
    {
        return typeof(T).GetMethod(methodName)?.GetParameters() // получим параметры метода,
            .Select(param => param.Name) // вытащим имена.
            .ToArray();
    }

    public string GetApiMethodParamDescription(string methodName, string paramName)
    {
        var methodType = typeof(T).GetMethod(methodName); // сам метод.
        if (methodType == null)
            return null; // вернем нулл, если такого нет.

        var paramType = methodType?.GetParameters() // берем его параметры.
            .Where(param => param.Name == paramName) // нам нужен конкретный,
            .Where(param => param.GetCustomAttribute<ApiDescriptionAttribute>() != null); // и чтобы в описании что-то было.

        if (paramType.Count() == 0) return null;
        return paramType
            .First()
            .GetCustomAttribute<ApiDescriptionAttribute>()
            .Description;
    }

    // вспомогательный метод. возвращает описание параметра.
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
            // пустое описание.
            return new ApiParamDescription() { ParamDescription = new CommonDescription(paramName) };

        ParameterInfo param = null;
        foreach (var p in methodType?.GetParameters())
            if (p.Name == paramName)
                param = p; // вытаскиваем нужный параметр.

        if (param == null)
            // пустое описание.
            return new ApiParamDescription() { ParamDescription = new CommonDescription(paramName) };

        // иначе вытаскиваем описание и возвращаем.
        return GetApiParamDescription(param);
    }

    public ApiMethodDescription GetApiMethodFullDescription(string methodName)
    {
        var methodType = typeof(T).GetMethod(methodName);
        // просто возвращаем нулл, если пусто.
        if (methodType == null)
            return null;
        if (methodType.GetCustomAttribute<ApiMethodAttribute>() == null)
            return null;

        // описание атрибутов.
        var result = new ApiMethodDescription();
        result.MethodDescription = new CommonDescription(methodName, GetApiMethodDescription(methodName));
        if (methodType.ReturnType != typeof(void))
            result.ReturnDescription = GetApiParamDescription(methodType.ReturnParameter);

        // описание параметров.
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
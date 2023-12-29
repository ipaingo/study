using NUnit.Framework.Constraints;
using System;
using System.Collections.Generic;
using System.Linq;

namespace linq_slideviews;

public class ParsingTask
{
	/// <param name="lines">Все строки файла, которые нужно распарсить. Первая строка - заголовочная.</param>
	/// <returns>Словарь: ключ — идентификатор слайда, значение — информация о слайде.</returns>
	/// <remarks>Метод должен пропускать некорректные строки, игнорируя их.</remarks>
	public static IDictionary<int, SlideRecord> ParseSlideRecords(IEnumerable<string> lines)
	{
		// хотела вынести все в отдельные методы, но на этапе придумывания названия осознала,
		// насколько бессмысленно оставлять этот метод состоящим из пяти строчек.

		return lines
			.Skip(1) // заголовочную строку пропускаем.
			.Select(l =>
			{
				// разделяем по точкам с запятой.
				var line = l.Split(';');

				// проверяем на корректность. если строка битая - будет нулл, иначе запись о слайде.
				if ((line.Length != 3) || (!int.TryParse(line[0], out int id)) ||
				(line[1].Length == 0))
					return null;


                line[1] = line[1].First().ToString().ToUpper() + String.Join("", line[1].Skip(1));
				if (!Enum.TryParse(line[1], out SlideType type))
					return null;

                return new SlideRecord(id, type, line[2]);
			})
			.Where(record => (record != null)) // нам нужно все, что не было отмечено битым.
			.ToDictionary(record => record.SlideId, record => record); // преобразуем в словарь id-запись.
	}

	/// <param name="lines">Все строки файла, которые нужно распарсить. Первая строка — заголовочная.</param>
	/// <param name="slides">Словарь информации о слайдах по идентификатору слайда.
	/// Такой словарь можно получить методом ParseSlideRecords.</param>
	/// <returns>Список информации о посещениях.</returns>
	/// <exception cref="FormatException">Если среди строк есть некорректные.</exception>
	public static IEnumerable<VisitRecord> ParseVisitRecords(
	IEnumerable<string> lines, IDictionary<int, SlideRecord> slides)
	{
		return lines
			.Skip(1) // заголовок пропускаем.
			.Select(line =>
			{
				var l = line.Split(';'); // разделяем по точкам с запятой.

				// проверяем на корректность. битая строка = исключение.
				if ((l.Length != 4) || (!int.TryParse(l[0], out int userId)) ||
				(!int.TryParse(l[1], out int slideId)) || (!DateTime.TryParse(l[2] + ' ' + l[3], out DateTime dateTime)) ||
				(!slides.ContainsKey(slideId)))
					throw new FormatException("Wrong line [" + line + "]");
				return new VisitRecord(userId, slideId, dateTime, slides[slideId].SlideType);
			});
	}
}

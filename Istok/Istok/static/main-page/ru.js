// ru.js
/* Russian locals for flatpickr */
var flatpickr = flatpickr || { l10ns: {} };
flatpickr.l10ns.ru = {};

flatpickr.l10ns.ru.weekdays = {
	shorthand: ["Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб"],
	longhand: [
		"Воскресенье",
		"Понедельник",
		"Вторник",
		"Среда",
		"Четверг",
		"Пятница",
		"Суббота",
	]
};

flatpickr.l10ns.ru.months = {
	shorthand: [
		"Янв",
		"Фев",
		"Март",
		"Апр",
		"Май",
		"Июнь",
		"Июль",
		"Авг",
		"Сен",
		"Окт",
		"Ноя",
		"Дек",
	],
	longhand: [
		"Январь",
		"Февраль",
		"Март",
		"Апрель",
		"Май",
		"Июнь",
		"Июль",
		"Август",
		"Сентябрь",
		"Октябрь",
		"Ноябрь",
		"Декабрь",
	],
};

flatpickr.l10ns.ru.firstDayOfWeek = 1;
flatpickr.l10ns.ru.rangeSeparator = " — ";
flatpickr.l10ns.ru.scrollTitle = "Прокрутите для увеличения";
flatpickr.l10ns.ru.toggleTitle = "Нажмите для переключения";

flatpickr.l10ns.ru.ordinal = function () {
	return "";
};

flatpickr.l10ns.ru.weekAbbreviation = "Нед.";
flatpickr.l10ns.ru.yearAriaLabel = "Год";

export default flatpickr.l10ns;

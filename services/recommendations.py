from config import DEFAULT_CATEGORIES, STATUSES


def calc_day_score(entry: dict) -> int:
    keys = [c["key"] for c in DEFAULT_CATEGORIES]
    score = 0
    for k in keys:
        val = entry.get(k, "none")
        if val == "yes":
            score += 2
        elif val == "partial":
            score += 1
    return score


def get_recommendation(entry: dict) -> str:
    tips = []
    score = calc_day_score(entry)
    max_score = len(DEFAULT_CATEGORIES) * 2

    if entry.get("sleep") == "no":
        tips.append("Сон - база всего. Попробуй лечь на 30 минут раньше сегодня.")
    elif entry.get("sleep") == "partial":
        tips.append("Сон был не идеальным. Проветри комнату и убери телефон за час до сна.")

    if entry.get("work") == "no":
        tips.append("Главная задача не сделана. Завтра начни с неё в первые 90 минут дня.")
    elif entry.get("work") == "partial":
        tips.append("Задача частично сделана - уже хорошо. Попробуй разбить её на мелкие шаги.")

    if entry.get("growth") == "no":
        tips.append("Развитие пропущено. Даже 15 минут чтения или видео - уже шаг вперёд.")

    if entry.get("sport") == "no":
        tips.append("Движение важно. Завтра хотя бы 20 минут прогулки.")
    elif entry.get("sport") == "partial":
        tips.append("Немного движения было. Попробуй добавить регулярность.")

    if entry.get("finance") == "no":
        tips.append("Финансы без внимания. Потрать 5 минут - запиши расходы за сегодня.")

    if entry.get("no_chaos") == "no":
        tips.append("Был хаос или самосаботаж. Запиши триггер - что именно сбило?")
    elif entry.get("no_chaos") == "partial":
        tips.append("Немного хаоса было. Подумай, какое одно правило поможет его избежать.")

    if entry.get("joy") == "no":
        tips.append("День без удовольствия - опасный путь. Запланируй завтра 1 приятное дело.")

    if score == max_score:
        header = "Идеальный день! Ты машина. Сохрани этот ритм."
    elif score >= max_score * 0.7:
        header = "Хороший день! Есть зоны роста, но фундамент крепкий."
    elif score >= max_score * 0.4:
        header = "Средний день. Не страшно, но завтра можно лучше."
    else:
        header = "Тяжёлый день. Главное - ты его отрефлексировал. Завтра новый старт."

    result = f"Оценка дня: {score}/{max_score}\n\n{header}"
    if tips:
        result += "\n\nСоветы:\n" + "\n".join(f"- {t}" for t in tips)

    return result


def format_entry_summary(entry: dict) -> str:
    lines = []
    for cat in DEFAULT_CATEGORIES:
        status = entry.get(cat["key"], "none")
        status_text = STATUSES.get(status, STATUSES["none"])
        lines.append(f'{cat["emoji"]} {cat["name"]}: {status_text}')

    score = calc_day_score(entry)
    lines.append(f'\nБаллы: {score}/{len(DEFAULT_CATEGORIES) * 2}')

    if entry.get("note"):
        lines.append(f'Заметка: {entry["note"]}')

    return "\n".join(lines)

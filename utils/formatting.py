def welcome_card(name: str) -> str:
    return (
        "╔══════════════════════════╗\n"
        f"   👋 Привет, <b>{name}</b>!\n"
        "╠══════════════════════════╣\n"
        "   Я твой трекер дня.\n"
        "\n"
        "   Каждый день отмечай\n"
        "   7 сфер жизни:\n"
        "\n"
        "   😴 Сон       🏋 Спорт\n"
        "   💼 Работа    💰 Финансы\n"
        "   📚 Развитие  🧹 Порядок\n"
        "   🎉 Радость\n"
        "\n"
        "   Получай советы и следи\n"
        "   за прогрессом! 📈\n"
        "╚══════════════════════════╝"
    )


def day_card(today: str, summary: str, subtitle: str) -> str:
    return (
        "┌─────────────────────────┐\n"
        f"   📅 <b>День: {today}</b>\n"
        "├─────────────────────────┤\n"
        f"{summary}\n"
        "├─────────────────────────┤\n"
        f"   {subtitle}\n"
        "└─────────────────────────┘"
    )


def today_card(today: str, summary: str, score: int) -> str:
    bar = score_bar(score, 14)
    return (
        "┌─────────────────────────┐\n"
        f"   📅 <b>Мой день: {today}</b>\n"
        "├─────────────────────────┤\n"
        f"{summary}\n"
        "├─────────────────────────┤\n"
        f"   Балл: {score}/14 {bar}\n"
        "└─────────────────────────┘"
    )


def finish_card(today: str, summary: str, recommendation: str, score: int) -> str:
    bar = score_bar(score, 14)
    if score >= 12:
        grade = "🏆 Отличный день!"
    elif score >= 8:
        grade = "👍 Хороший день!"
    elif score >= 5:
        grade = "💪 Можно лучше!"
    else:
        grade = "🔥 Завтра будет лучше!"
    return (
        "╔══════════════════════════╗\n"
        f"   🏁 <b>День завершён!</b>\n"
        f"   {today}\n"
        "╠══════════════════════════╣\n"
        f"{summary}\n"
        "╠══════════════════════════╣\n"
        f"   Балл: {score}/14 {bar}\n"
        f"   {grade}\n"
        "╠══════════════════════════╣\n"
        f"   💡 <b>Совет:</b>\n"
        f"   {recommendation}\n"
        "╚══════════════════════════╝"
    )


def note_saved_card(summary: str) -> str:
    return (
        "┌─────────────────────────┐\n"
        "   💬 <b>Заметка сохранена!</b>\n"
        "├─────────────────────────┤\n"
        f"{summary}\n"
        "└─────────────────────────┘"
    )


def recommendation_card(recommendation: str) -> str:
    return (
        "╔══════════════════════════╗\n"
        "   💡 <b>Рекомендация</b>\n"
        "╠══════════════════════════╣\n"
        f"   {recommendation}\n"
        "╚══════════════════════════╝"
    )


def week_stats_card(date_from: str, date_to: str, days_data: list) -> str:
    total = sum(s for _, s in days_data)
    count = len(days_data)
    avg = round(total / count, 1) if count else 0

    lines = ""
    for d, s in days_data:
        bar = score_bar(s, 14)
        lines += f"   {d}: {s}/14 {bar}\n"

    if avg >= 10:
        verdict = "🏆 Отличная неделя!"
    elif avg >= 6:
        verdict = "👍 Неплохо, есть куда расти!"
    else:
        verdict = "🔥 Ты отслеживаешь — это уже шаг!"

    return (
        "╔══════════════════════════╗\n"
        f"   📊 <b>Неделя</b>\n"
        f"   {date_from} — {date_to}\n"
        "╠══════════════════════════╣\n"
        f"{lines}"
        "╠══════════════════════════╣\n"
        f"   Дней: {count} | Средний: {avg}/14\n"
        f"   {verdict}\n"
        "╚══════════════════════════╝"
    )


def score_bar(score: int, max_score: int) -> str:
    filled = round(score / max_score * 7) if max_score else 0
    empty = 7 - filled
    return "▓" * filled + "░" * empty

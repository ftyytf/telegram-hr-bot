// === Telegram WebApp Init ===
const tg = window.Telegram ? window.Telegram.WebApp : null;
if (tg) {
    tg.ready();
    tg.expand();
}

// === Checklist Data by Week ===
const checklistByWeek = {
    1: [
        'Познакомиться с командой',
        'Настроить рабочее место',
        'Получить доступы к системам',
        'Прочитать welcome-гайд',
        'Найти наставника/бадди'
    ],
    2: [
        'Изучить основные процессы',
        'Пройти обязательные курсы',
        'Провести 1-on-1 с руководителем',
        'Познакомиться со смежными отделами',
        'Задать накопившиеся вопросы'
    ],
    3: [
        'Взять первую рабочую задачу',
        'Изучить документацию проекта',
        'Посетить командную встречу',
        'Настроить рабочие инструменты',
        'Дать обратную связь по онбордингу'
    ],
    4: [
        'Завершить первую задачу',
        'Провести демо результатов',
        'Составить план развития',
        'Оценить свой прогресс',
        'Обсудить впечатления с HR'
    ]
};

// === State ===
let currentMood = 0;
let checkedItems = new Set();
let savedDays = JSON.parse(localStorage.getItem('hrbuddy_days') || '[]');

// === Helpers ===
function getCurrentWeek() {
    if (tg && tg.initDataUnsafe && tg.initDataUnsafe.start_param) {
        const week = parseInt(tg.initDataUnsafe.start_param);
        if (week >= 1 && week <= 4) return week;
    }
    const totalDays = savedDays.length;
    return Math.min(Math.floor(totalDays / 7) + 1, 4);
}

function getTodayKey() {
    return new Date().toISOString().split('T')[0];
}

function isTodaySaved() {
    return savedDays.some(function(d) { return d.date === getTodayKey(); });
}

// === Tabs ===
document.querySelectorAll('.tab').forEach(function(tab) {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
        document.querySelectorAll('.page').forEach(function(p) { p.classList.remove('active'); });
        tab.classList.add('active');
        var target = tab.getAttribute('data-tab');
        document.getElementById(target).classList.add('active');

        if (target === 'history') renderHistory();
        if (target === 'stats') renderStats();
    });
});

// === Checklist ===
function renderChecklist() {
    var week = getCurrentWeek();
    var items = checklistByWeek[week] || checklistByWeek[1];
    var container = document.getElementById('checklist');
    container.innerHTML = '';

    if (isTodaySaved()) {
        container.innerHTML = '<div class="empty-state">Сегодня уже сохранено! Приходи завтра.</div>';
        document.getElementById('save-btn').style.display = 'none';
        document.querySelector('.mood-section').style.display = 'none';
        return;
    }

    items.forEach(function(text, index) {
        var div = document.createElement('div');
        div.className = 'check-item' + (checkedItems.has(index) ? ' done' : '');
        div.innerHTML = '<div class="check-box"></div><span class="check-text">' + text + '</span>';
        div.addEventListener('click', function() {
            if (checkedItems.has(index)) {
                checkedItems.delete(index);
            } else {
                checkedItems.add(index);
            }
            renderChecklist();
        });
        container.appendChild(div);
    });
}

// === Mood ===
document.querySelectorAll('.mood-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
        document.querySelectorAll('.mood-btn').forEach(function(b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        currentMood = parseInt(btn.getAttribute('data-mood'));
        var labels = {1: 'Очень плохо', 2: 'Плохо', 3: 'Нормально', 4: 'Хорошо', 5: 'Отлично!'};
        document.getElementById('mood-status').textContent = labels[currentMood] || '';
    });
});

// === Save ===
document.getElementById('save-btn').addEventListener('click', function() {
    if (currentMood === 0) {
        alert('Выбери настроение!');
        return;
    }

    var week = getCurrentWeek();
    var items = checklistByWeek[week] || checklistByWeek[1];

    var dayData = {
        date: getTodayKey(),
        week: week,
        mood: currentMood,
        done: checkedItems.size,
        total: items.length
    };

    savedDays.push(dayData);
    localStorage.setItem('hrbuddy_days', JSON.stringify(savedDays));

    // Send to bot if in Telegram
    if (tg) {
        tg.sendData(JSON.stringify(dayData));
    }

    checkedItems.clear();
    currentMood = 0;
    renderChecklist();
    alert('День сохранён!');
});

// === History ===
function renderHistory() {
    var container = document.getElementById('history-list');
    if (savedDays.length === 0) {
        container.innerHTML = '<div class="empty-state">Пока нет записей. Заполни первый день!</div>';
        return;
    }

    var html = '';
    var sorted = savedDays.slice().reverse();
    sorted.forEach(function(day) {
        var moods = ['', '\u{1F62B}', '\u{1F615}', '\u{1F610}', '\u{1F642}', '\u{1F60A}'];
        html += '<div class="history-item">';
        html += '<div class="history-date">' + day.date + ' ' + moods[day.mood] + '</div>';
        html += '<div class="history-details">Неделя ' + day.week + ' \u2022 Выполнено: ' + day.done + '/' + day.total + '</div>';
        html += '<div class="progress-bar"><div class="progress-fill" style="width:' + Math.round(day.done/day.total*100) + '%"></div></div>';
        html += '</div>';
    });
    container.innerHTML = html;
}

// === Stats ===
function renderStats() {
    var container = document.getElementById('stats-content');
    if (savedDays.length === 0) {
        container.innerHTML = '<div class="empty-state">Нужна хотя бы одна запись для статистики</div>';
        return;
    }

    var totalDays = savedDays.length;
    var avgMood = savedDays.reduce(function(s, d) { return s + d.mood; }, 0) / totalDays;
    var totalDone = savedDays.reduce(function(s, d) { return s + d.done; }, 0);
    var totalTasks = savedDays.reduce(function(s, d) { return s + d.total; }, 0);
    var completion = Math.round(totalDone / totalTasks * 100);

    var moods = ['', '\u{1F62B}', '\u{1F615}', '\u{1F610}', '\u{1F642}', '\u{1F60A}'];
    var moodEmoji = moods[Math.round(avgMood)] || '\u{1F610}';

    var html = '';
    html += '<div class="stats-card"><div class="stats-number">' + totalDays + '</div><div class="stats-label">дней трекинга</div></div>';
    html += '<div class="stats-card"><div class="stats-number">' + moodEmoji + ' ' + avgMood.toFixed(1) + '</div><div class="stats-label">среднее настроение</div></div>';
    html += '<div class="stats-card"><div class="stats-number">' + completion + '%</div><div class="stats-label">задач выполнено</div><div class="progress-bar"><div class="progress-fill" style="width:' + completion + '%"></div></div></div>';
    html += '<div class="stats-card"><div class="stats-number">' + getCurrentWeek() + '/4</div><div class="stats-label">текущая неделя</div></div>';

    container.innerHTML = html;
}

// === Init ===
renderChecklist();

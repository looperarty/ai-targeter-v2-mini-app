const telegramWebApp = window.Telegram.WebApp;

telegramWebApp.ready();
telegramWebApp.expand();

// --- Логика для кнопок хедера ---

document.getElementById('backButton').addEventListener('click', () => {
    telegramWebApp.close(); // Закрываем Mini App
});

document.getElementById('calendarButton').addEventListener('click', () => {
    // В будущем здесь будет логика для выпадающего календаря
    telegramWebApp.showAlert(`Кнопка "Выбор даты" нажата. Сегодня: ${new Date().toLocaleDateString()}`);
});

document.getElementById('refreshButton').addEventListener('click', () => {
    // Здесь можно добавить логику для обновления данных
    telegramWebApp.showAlert('Данные обновлены (функция в разработке).');
    // В реальном приложении здесь будет запрос к боту за новыми данными
});

document.getElementById('themeToggleButton').addEventListener('click', () => {
    // Логика для переключения темы (темная/светлая)
    // Telegram Web Apps автоматически предоставляет информацию о теме.
    // Можно получить ее через telegramWebApp.themeParams и менять стили динамически.
    const isDark = telegramWebApp.colorScheme === 'dark';
    const newTheme = isDark ? 'светлая' : 'темная';
    telegramWebApp.showAlert(`Тема будет переключена на ${newTheme}. (Функционал в разработке. Сейчас тема определяется настройками Telegram.)`);

    // Более продвинутый способ: отправить запрос Telegram на изменение темы
    // telegramWebApp.sendData(JSON.stringify({ type: 'toggle_theme' }));
    // Или просто переключать класс на body для кастомных стилей
});


// --- Логика для кнопок статистики (показ описания) ---
document.querySelectorAll('.stat-card').forEach(button => {
    const description = button.querySelector('.metric-description');
    if (description) {
        button.addEventListener('click', () => {
            // Переключаем видимость описания
            description.classList.toggle('visible');
            // Можно добавить задержку, чтобы описание само исчезало
            // setTimeout(() => {
            //     description.classList.remove('visible');
            // }, 3000);
        });
    }
});


// --- Логика для отправки данных формы (оставлена для тестов) ---
document.getElementById('analyzeButton').addEventListener('click', () => {
    const productName = document.getElementById('productName').value.trim();
    const campaignGoal = document.getElementById('campaignGoal').value;
    const targetAudienceDesc = document.getElementById('targetAudienceDesc').value.trim();
    const budget = document.getElementById('budget').value.trim();

    if (!productName || !campaignGoal) {
        telegramWebApp.showAlert('Пожалуйста, введите название продукта и выберите цель кампании.');
        return;
    }

    const data = {
        type: 'campaign_analysis_manual', // Изменил тип запроса
        product_name: productName,
        campaign_goal: campaignGoal,
        target_audience_description: targetAudienceDesc,
        budget: budget,
        timestamp: new Date().toISOString()
    };

    // Отправляем данные боту
    telegramWebApp.sendData(JSON.stringify(data));

    telegramWebApp.close(); // Закрываем Mini App после отправки данных
});
const telegramWebApp = window.Telegram.WebApp;

telegramWebApp.ready();
telegramWebApp.expand();

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
        type: 'campaign_analysis', // Тип запроса для бэкенда
        product_name: productName,
        campaign_goal: campaignGoal,
        target_audience_description: targetAudienceDesc,
        budget: budget,
        timestamp: new Date().toISOString()
    };

    // Отправляем данные боту
    telegramWebApp.sendData(JSON.stringify(data));

    telegramWebApp.close(); // Можно закрыть Mini App после отправки данных
});
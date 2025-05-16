/**
 * WeatherAPI.comからデータを取得する関数
 */
async function fetchWeatherData(apiKey, lat, lon) {
    const response = await fetch(
        `https://api.weatherapi.com/v1/forecast.json?key=${apiKey}&q=${lat},${lon}&days=3&lang=ja&aqi=no`
    );

    if (!response.ok) {
        throw new Error("天気データの取得に失敗しました");
    }

    return await response.json();
}


function updateCurrentWeather(element, current, today) {
    const currentTemp = Math.round(current.temp_c);
    const todayMaxTemp = Math.round(today.day.maxtemp_c);

    const iconElement = element.querySelector('.weather-icon');
    iconElement.src = current.condition.icon; // WeatherAPIのアイコンを使用

    element.querySelector('.description').textContent = current.condition.text;
    element.querySelector('.temp-range').textContent = `${currentTemp}°C/${todayMaxTemp}°C`;
}

function updateForecastItem(element, forecast) {
    element.querySelector('.max').textContent = `${Math.round(forecast.day.maxtemp_c)}°C`;
    
    const iconElement = element.querySelector('.weather-icon');
    iconElement.src = forecast.day.condition.icon; // WeatherAPIのアイコンを使用
    
    element.querySelector('.description').textContent = forecast.day.condition.text;
}

/**
 * 天気情報を更新する関数
 */
async function updateWeatherDisplay() {
    const { apiKey, location } = WEATHER_CONFIG;
    const { lat, lon } = location;
    
    try {
        const data = await fetchWeatherData(apiKey, lat, lon);
        console.log('WeatherAPI データ:', data);

        // 現在の天気を更新
        const currentWeather = document.querySelector('.current-weather');
        updateCurrentWeather(currentWeather, data.current, data.forecast.forecastday[0]);

        // 予報を更新
        const forecastItems = document.querySelectorAll('.forecast-item');
        if (forecastItems[0]) {
            updateForecastItem(forecastItems[0], data.forecast.forecastday[1]);
        }
        if (forecastItems[1]) {
            updateForecastItem(forecastItems[1], data.forecast.forecastday[2]);
        }

    } catch (err) {
        console.error("天気データの取得に失敗:", err);
        const currentWeather = document.querySelector('.current-weather');
        currentWeather.querySelector('.description').textContent = "天気データの取得に失敗しました";
    }
}

// 初期化処理と定期更新の設定
document.addEventListener("DOMContentLoaded", () => {
    // 初回の天気情報取得
    updateWeatherDisplay();
    
    // 30分ごとに天気情報を更新
    const WEATHER_UPDATE_INTERVAL = 30 * 60 * 1000; // 30分
    setInterval(updateWeatherDisplay, WEATHER_UPDATE_INTERVAL);
});

setInterval(() => {
    // pi zero 2wだとanimationでCPU100%になるので、1分ごとにリセット
    document.querySelectorAll('.weather-icon').forEach(el => {
        el.classList.remove('animate-pulse');
        void el.offsetWidth;
        el.classList.add('animate-pulse');
    });
}, 60000); // 1分ごと
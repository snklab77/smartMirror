document.addEventListener("DOMContentLoaded", () => {
  const weatherEl = document.getElementById("weather-widget");

  async function fetchWeather() {
    const { apiKey, city, units, lang } = WEATHER_CONFIG;
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=${units}&lang=${lang}`;

    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error("HTTP error " + response.status);
      const data = await response.json();
      const temp = Math.round(data.main.temp);
      const description = data.weather[0].description;
      weatherEl.textContent = `${description}・${temp}°C`;
    } catch (err) {
      weatherEl.textContent = "天気取得失敗";
      console.error("Weather fetch error:", err);
    }
  }

  fetchWeather();
  setInterval(fetchWeather, 1000 * 60 * 10); // 10分ごとに更新
});
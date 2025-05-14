/**
 * 各種設定を定義する
 */

/*
* WeatherAppの設定
*/
const WEATHER_CONFIG = {
  // OpenWeatherMapのAPIキー
  apiKey: ENV.OPENWEATHER_API_KEY,
  city: "Tokyo",
  // "metric" for 摂氏（℃）, "imperial" 華氏（°F）default: "standard" ケルビン (K)
  units: "metric",
  lang: "ja"
};
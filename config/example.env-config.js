/**
 * 環境変数
 */
const ENV = {
  /*
  * weatherapiのAPI KEY設定
  * https://www.weatherapi.com/
  * weatherapiのAPIキーを取得するには、上記のURLにアクセスしてアカウントを作成してください。
  * APIキーは、アカウント作成後にダッシュボードから取得できます。
  */
  WEATHERAPI_KEY: "YOUR-API-KEY-HERE",

  /*
  * 位置情報設定
  * 緯度経度は小数点以下6桁程度まで指定可能です
  */
  LOCATION: {
    lat: 35.681143654455774,
    lon: 139.76749021382773,
    name: "品川区"
  }
};
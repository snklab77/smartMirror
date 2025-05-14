
document.addEventListener("DOMContentLoaded", () => {
  const clockEl = document.getElementById("clock");
  const warekiEl = document.getElementById("wareki");
  const gregorianEl = document.getElementById("gregorianYear");
  const dateLabelEl = document.getElementById("month-day");

  function getWareki(year) {
    if (year >= 2019) {
      return `令和${year - 2018}年`;
    } else if (year >= 1989) {
      return `平成${year - 1988}年`;
    } else {
      return `${year}年`;
    }
  }

  function updateDate() {
    const now = dayjs();

    const wareki = getWareki(now.year());
    const gregorianYear = `${now.year()}`;
    const dateLabel = now.format('M月D日(dd)');
    const timeStr = now.format('HH:mm');

    if (warekiEl) warekiEl.textContent = wareki;
    if (gregorianEl) gregorianEl.textContent = gregorianYear;
    if (dateLabelEl) dateLabelEl.textContent = dateLabel;
    if (clockEl) clockEl.textContent = timeStr;
  }

  setInterval(updateDate, 1000);
  updateDate();
});
const emailLink = document.querySelector("#emailOrder");
const packSelect = document.querySelector("#packSelect");
const cityInput = document.querySelector("#cityInput");
const timeInput = document.querySelector("#timeInput");
const noteInput = document.querySelector("#noteInput");
const packCards = document.querySelectorAll("[data-pack]");

function updateEmailLink() {
  const pack = packSelect?.value || "6 尾家庭包";
  const city = cityInput?.value || "";
  const time = timeInput?.value || "";
  const note = noteInput?.value || "";
  const body = [
    "我想預購一尾一餐家常魚",
    "",
    `預購包裝：${pack}`,
    `收件縣市：${city}`,
    `可收貨時間：${time}`,
    `備註：${note}`,
    "",
    "請客服協助確認魚種、產地、售價、出貨日與低溫配送方式。"
  ].join("\n");

  emailLink.href = `mailto:hello@example.com?subject=${encodeURIComponent("一尾一餐家常魚預購")}&body=${encodeURIComponent(body)}`;
}

packCards.forEach((card) => {
  card.addEventListener("click", (event) => {
    const pack = card.getAttribute("data-pack");
    if (packSelect && pack) {
      packSelect.value = pack;
      updateEmailLink();
    }
    if (event.target.tagName !== "A") {
      document.querySelector("#order")?.scrollIntoView({ behavior: "smooth" });
    }
  });
});

[packSelect, cityInput, timeInput, noteInput].forEach((field) => {
  field?.addEventListener("input", updateEmailLink);
  field?.addEventListener("change", updateEmailLink);
});

updateEmailLink();

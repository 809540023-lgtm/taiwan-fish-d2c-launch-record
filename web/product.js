const emailLink = document.querySelector("#emailOrder");
const copyButton = document.querySelector("#copyOrder");
const packSelect = document.querySelector("#packSelect");
const cityInput = document.querySelector("#cityInput");
const timeInput = document.querySelector("#timeInput");
const noteInput = document.querySelector("#noteInput");
const messagePreview = document.querySelector("#messagePreview");
const copyStatus = document.querySelector("#copyStatus");
const summaryPack = document.querySelector("#summaryPack");
const summaryWeight = document.querySelector("#summaryWeight");
const summaryHint = document.querySelector("#summaryHint");
const orderSection = document.querySelector("#order");
const stickyOrder = document.querySelector(".sticky-order");
const packCards = document.querySelectorAll("[data-pack]");

const fallbackPacks = {
  "3 尾體驗包": {
    weight: "約 900g",
    hint: "先試乾煎和魚湯口感，適合首購試吃。"
  },
  "6 尾家庭包": {
    weight: "約 1.8kg",
    hint: "小家庭一週晚餐常備，是主力推薦組合。"
  },
  "10 尾常備包": {
    weight: "約 3kg",
    hint: "適合固定煮飯家庭，一次把平日晚餐補進冰箱。"
  },
  "20 尾團購箱": {
    weight: "約 6kg",
    hint: "適合社區、公司、親友團，客服會協助確認分箱與配送。"
  }
};

function getPackInfo(pack) {
  const selectedCard = [...packCards].find((card) => card.dataset.pack === pack);
  return {
    weight: selectedCard?.dataset.weight || fallbackPacks[pack]?.weight || "客服確認",
    hint: selectedCard?.dataset.hint || fallbackPacks[pack]?.hint || "客服會協助確認規格、售價與出貨。"
  };
}

function buildOrderMessage() {
  const pack = packSelect?.value || "6 尾家庭包";
  const city = cityInput?.value.trim() || "待填";
  const time = timeInput?.value.trim() || "待填";
  const note = noteInput?.value.trim() || "無";
  const info = getPackInfo(pack);

  return [
    "我想預購一尾一餐家常魚",
    "",
    `預購包裝：${pack}`,
    `預估重量：${info.weight}`,
    `收件縣市：${city}`,
    `可收貨時間：${time}`,
    `備註：${note}`,
    "",
    "請客服協助確認魚種、產地、售價、出貨日與低溫配送方式。"
  ].join("\n");
}

function updateSelectedCard(pack) {
  packCards.forEach((card) => {
    card.classList.toggle("selected", card.dataset.pack === pack);
  });
}

function updateOrderState() {
  const pack = packSelect?.value || "6 尾家庭包";
  const info = getPackInfo(pack);
  const message = buildOrderMessage();

  if (summaryPack) summaryPack.textContent = pack;
  if (summaryWeight) summaryWeight.textContent = info.weight;
  if (summaryHint) summaryHint.textContent = info.hint;
  if (messagePreview) messagePreview.value = message;
  if (emailLink) {
    emailLink.href = `mailto:hello@example.com?subject=${encodeURIComponent("一尾一餐家常魚預購")}&body=${encodeURIComponent(message)}`;
  }

  updateSelectedCard(pack);
}

function fallbackCopy() {
  messagePreview?.focus();
  messagePreview?.select();
  document.execCommand("copy");
}

packCards.forEach((card) => {
  card.addEventListener("click", (event) => {
    const pack = card.dataset.pack;
    if (packSelect && pack) {
      packSelect.value = pack;
      updateOrderState();
    }
    const clickedLink = event.target instanceof Element && event.target.closest("a");
    if (!clickedLink) {
      document.querySelector("#order")?.scrollIntoView({ behavior: "smooth" });
    }
  });
});

[packSelect, cityInput, timeInput, noteInput].forEach((field) => {
  field?.addEventListener("input", updateOrderState);
  field?.addEventListener("change", updateOrderState);
});

copyButton?.addEventListener("click", async () => {
  const message = buildOrderMessage();
  try {
    await navigator.clipboard.writeText(message);
  } catch {
    fallbackCopy();
  }

  if (copyStatus) {
    copyStatus.textContent = "已複製，可貼到 LINE 或 FB 私訊。";
  }
});

if (orderSection && stickyOrder && "IntersectionObserver" in window) {
  const orderObserver = new IntersectionObserver(
    ([entry]) => {
      stickyOrder.classList.toggle("is-hidden", entry.isIntersecting);
    },
    { threshold: 0.08 }
  );

  orderObserver.observe(orderSection);
}

updateOrderState();

document.addEventListener("DOMContentLoaded", () => {
  const widget = document.getElementById("quotes-widget");
  if (!widget) return;

  const quotesDataStr = widget.getAttribute("data-quotes");
  if (!quotesDataStr) return;

  let quotes = [];
  try {
    quotes = JSON.parse(quotesDataStr);
  } catch (e) {
    console.error("Failed to parse quotes data", e);
    return;
  }

  if (quotes.length === 0) return;

  const textEl = document.getElementById("quote-text");
  const attrEl = document.getElementById("quote-attribution");

  let currentIndex = 0;

  function renderQuote(index) {
    const q = quotes[index];
    textEl.style.opacity = 0;
    attrEl.style.opacity = 0;
    setTimeout(() => {
      textEl.textContent = `"${q.text}"`;
      attrEl.textContent = `— ${q.attribution}`;
      textEl.style.opacity = 1;
      attrEl.style.opacity = 1;
    }, 300);
  }

  renderQuote(currentIndex);

  setInterval(() => {
    currentIndex = (currentIndex + 1) % quotes.length;
    renderQuote(currentIndex);
  }, 10000);
});

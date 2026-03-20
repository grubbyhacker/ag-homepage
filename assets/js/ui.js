document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("theme-toggle");
  if (!toggleBtn) return;
  const moonIcon = toggleBtn.querySelector(".icon-moon");
  const sunIcon = toggleBtn.querySelector(".icon-sun");

  function updateIcons(theme) {
    if (theme === "dark") {
      moonIcon.style.display = "none";
      sunIcon.style.display = "block";
    } else {
      moonIcon.style.display = "block";
      sunIcon.style.display = "none";
    }
  }

  updateIcons(document.documentElement.getAttribute("data-theme"));

  toggleBtn.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const targetTheme = currentTheme === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", targetTheme);
    localStorage.setItem("theme", targetTheme);
    updateIcons(targetTheme);

    const darkChroma = document.getElementById("chroma-dark");
    const lightChroma = document.getElementById("chroma-light");
    if (darkChroma && lightChroma) {
      if (targetTheme === "dark") {
        darkChroma.media = "all";
        lightChroma.media = "not all";
      } else {
        lightChroma.media = "all";
        darkChroma.media = "not all";
      }
    }
  });
});

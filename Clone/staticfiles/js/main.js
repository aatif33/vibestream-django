document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-toggle-password]").forEach((button) => {
    button.addEventListener("click", () => {
      const input = document.getElementById(button.dataset.togglePassword);
      if (!input) return;
      const show = input.type === "password";
      input.type = show ? "text" : "password";
      button.textContent = show ? "Hide" : "Show";
    });
  });

  const audio = document.getElementById("audio-player");
  document.querySelectorAll("[data-audio]").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!audio) return;
      const url = button.dataset.audio;
      if (audio.src === new URL(url, window.location.href).href && !audio.paused) {
        audio.pause();
        button.textContent = "▶";
        return;
      }
      document.querySelectorAll("[data-audio]").forEach((other) => other.textContent = "▶");
      audio.src = url;
      try {
        await audio.play();
        button.textContent = "Ⅱ";
      } catch (error) {
        console.warn("This audio URL could not be played.", error);
        alert("This track could not be played. Check that the audio URL is a direct, playable audio file.");
      }
    });
  });
  if (audio) {
    audio.addEventListener("ended", () => document.querySelectorAll("[data-audio]").forEach((button) => button.textContent = "▶"));
    audio.addEventListener("pause", () => document.querySelectorAll("[data-audio]").forEach((button) => button.textContent = "▶"));
  }

  document.querySelectorAll(".message").forEach((message) => {
    window.setTimeout(() => {
      message.classList.add("message-hide");
      window.setTimeout(() => message.remove(), 350);
    }, 4500);
  });
});

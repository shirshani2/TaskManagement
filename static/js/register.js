document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.getElementById("registerForm");
  const errorMessage = document.getElementById("errorMessage");

  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      errorMessage.textContent = "הסיסמאות אינן תואמות";
      return;
    }

    try {
      const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        const telegramCode = data.telegram_verification_code;
        const telegramCodeElement = document.getElementById("telegramCode");

        telegramCodeElement.innerHTML = `
          <p>✅ נרשמת בהצלחה!</p>
          <p>כדי לקבל עדכונים בטלגרם:</p>
          <ol>
            <li>לחצי <a href="https://web.telegram.org/k/#@ShirsTaskBot" target="_blank">כאן</a> כדי לפתוח את הבוט בגרסת אינטרנט</li>
            <li>לחצי על <strong>START</strong></li>
            <li>והדביקי את הקוד הבא:</li>
          </ol>
          <div style="direction:ltr; margin-bottom: 10px;">
            <code id="codeToCopy">${telegramCode}</code>
            <button onclick="copyToClipboard('${telegramCode}')">📋 העתק</button>
          </div>
        `;

        registerForm.reset();
      } else {
        errorMessage.textContent = data.error || "אירעה שגיאה בעת ההרשמה";
      }
    } catch (error) {
      errorMessage.textContent = "אירעה שגיאה, אנא נסה שוב מאוחר יותר";
      console.error("Registration error:", error);
    }
  });
});

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    alert("✅ הקוד הועתק");
  });
}

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
    
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        errorMessage.textContent = errorData.error || "אירעה שגיאה בעת ההרשמה";
        return;
      }
    
      const data = await response.json();
    
      // בדיקה שהטוקן אכן קיים
      if (!data.access_token) {
        errorMessage.textContent = "לא התקבל טוקן גישה מהשרת";
        return;
      }
    
      const telegramCode = data.telegram_verification_code;
      const accessToken = data.access_token;
      showSuccessPopup(telegramCode, accessToken);
      registerForm.reset();
    
    } catch (error) {
      errorMessage.textContent = "אירעה שגיאה, אנא נסה שוב מאוחר יותר";
      console.error("Registration error:", error);
    }
    
  });
});

function showSuccessPopup(telegramCode, accessToken) {
  const popup = document.createElement("div");
  popup.className = "popup-success";

  popup.innerHTML = `
    <h3>🎉 ההרשמה הושלמה!</h3>
    <p>כדי לקבל עדכונים בטלגרם:</p>
    <ol>
      <li>לחצו <a href="https://web.telegram.org/k/#@ShirsTaskBot" target="_blank">כאן</a> כדי לפתוח את הבוט</li>
      <li>כתבו <code>START</code> בצ'אט</li>
      <li>שלחו את הקוד: <strong style="direction:ltr">${telegramCode}</strong></li>
    </ol>
    <div style="margin-top: 20px;">
      <button class="copy-btn" onclick="copyToClipboard(this, '${telegramCode}')">📋 העתק קוד</button>
      <button class="close-popup">✖ סגור</button>
    </div>
  `;

  document.body.appendChild(popup);

  const closeBtn = popup.querySelector(".close-popup");
  closeBtn.addEventListener("click", () => {
    localStorage.setItem("token", accessToken);
    window.location.href = "/tasks";
  });
}


// פונקציה להעתקת הקוד והצגת הודעת Toast
function copyToClipboard(button, text) {
  navigator.clipboard.writeText(text).then(() => {
    // עדכון טקסט הכפתור לכמה שניות
    const original = button.textContent;
    button.textContent = "✅ הועתק!";
    setTimeout(() => (button.textContent = original), 2000);
    showToast("הקוד הועתק בהצלחה 🎉");
  });
}

// פונקציה להצגת הודעת Toast
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.textContent = message;
  document.body.appendChild(toast);

  // הצגת ה-toast
  setTimeout(() => toast.classList.add("show"), 10);
  // הסרת ה-toast לאחר 3 שניות
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

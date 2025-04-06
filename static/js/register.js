document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");
    const errorMessage = document.getElementById("errorMessage");
    
    registerForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      
      const name = document.getElementById("name").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirmPassword").value;
      
      // בדיקת תקינות הקלט
      if (password !== confirmPassword) {
        errorMessage.textContent = "הסיסמאות אינן תואמות";
        return;
      }
      
      // שליחת בקשת הרשמה ל-API
      try {
        const response = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ name, email, password }),
        });
        
        const data = await response.json();
        
        if (response.ok) {
          // הרשמה הצליחה, הפניה לדף התחברות
          alert("ההרשמה הצליחה! עכשיו תוכל להתחבר.");
          window.location.href = "/";
        } else {
          // הצגת שגיאה למשתמש
          errorMessage.textContent = data.error || "אירעה שגיאה בעת ההרשמה";
        }
      } catch (error) {
        errorMessage.textContent = "אירעה שגיאה, אנא נסה שוב מאוחר יותר";
        console.error("Registration error:", error);
      }
    });
  });
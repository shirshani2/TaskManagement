    document.addEventListener("DOMContentLoaded", () => {
      const loginForm = document.getElementById("loginForm");
      const errorMessage = document.getElementById("errorMessage");
      
      
      
      loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        
        // שליחת בקשת התחברות ל-API
        try {
          const response = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
          });
          
          const data = await response.json();
          
          if (response.ok) {
            // שמירת טוקן ומעבר לדף המשימות
            localStorage.setItem("token", data.access_token);
            window.location.href = "/tasks";
          } else {
            // הצגת שגיאה למשתמש
            errorMessage.textContent = data.error || "אימייל או סיסמה שגויים";
          }
        } catch (error) {
          errorMessage.textContent = "אירעה שגיאה, אנא נסה שוב מאוחר יותר";
          console.error("Login error:", error);
        }
      });
    });

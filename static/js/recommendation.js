async function fetchRecommendation() {
    const token = localStorage.getItem("token");
  
    if (!token) {
      window.location.href = "/";
      return;
    }
  
    try {
        const res = await fetch("/api/ai/recommend", {
            method: "POST",
            headers: {
              "Authorization": "Bearer " + token
            }
          });
  
      const text = await res.text();
      const content = document.getElementById("recommendationContent");
  
      if (res.ok) {
        const data = JSON.parse(text);
        content.textContent = data.recommendation;
      } else {
        content.textContent = "שגיאה בשרת:\n" + text;
        console.error("שגיאה מהשרת:", text);
      }
    } catch (error) {
      document.getElementById("recommendationContent").textContent = "שגיאה בחיבור לשרת.";
      console.error("שגיאת רשת:", error);
    }
  }
  
  document.addEventListener("DOMContentLoaded", fetchRecommendation);
  
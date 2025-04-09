// בדיקה אם המשתמש מחובר
function checkAuth() {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "/";
  }
  return token;
}

// קבלת כל המשימות מה-API
async function getTasks() {
  const token = checkAuth();
  try {
    const res = await fetch("/api/tasks/", {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      throw new Error("Failed to fetch tasks");
    }

    const tasks = await res.json();
    displayTasks(tasks);
  } catch (error) {
    showMessage("שגיאה בטעינת המשימות: " + error.message, "error");
  }
}

// הצגת המשימות על המסך
function displayTasks(tasks) {
  const tasksList = document.getElementById("tasksList");
  const statusFilter = document.getElementById("statusFilter").value;

  tasksList.innerHTML = "";

  const filteredTasks = statusFilter === "all"
    ? tasks
    : tasks.filter(task => task.status === statusFilter);

  if (filteredTasks.length === 0) {
    tasksList.innerHTML = "<div class='no-tasks'>אין משימות להצגה</div>";
    return;
  }

  filteredTasks.forEach(task => {
    const template = document.getElementById("taskTemplate");
    const taskElement = document.importNode(template.content, true);

    taskElement.querySelector(".task-title").textContent = task.title;
    taskElement.querySelector(".task-status").textContent = getStatusText(task.status);
    taskElement.querySelector(".task-status").className = `task-status ${task.status}`;

    if (task.description) {
      taskElement.querySelector(".task-description").textContent = task.description;
    } else {
      taskElement.querySelector(".task-description").style.display = "none";
    }

    const taskItem = taskElement.querySelector(".task-item");
    taskItem.dataset.id = task._id;

    if (task.status === "completed") {
      taskItem.classList.add("bg-green");
    }

    // 🎨 צבע רקע לפי מצב תאריך יעד
    if (task.due_date) {
      const dueDate = new Date(task.due_date);
      const today = new Date();
      today.setHours(0, 0, 0, 0);
    
      const timeDiff = dueDate.setHours(0, 0, 0, 0) - today.getTime(); // השוואת תאריכים רק לפי יום
      const oneDay = 24 * 60 * 60 * 1000;
    
      // ניקוי רקע קודם אם יש
      taskItem.classList.remove("bg-red", "bg-orange", "bg-yellow", "bg-blue", "bg-green");
    
      if (timeDiff > 0) {
        taskItem.classList.add("bg-red"); // עבר הזמן
      } else if (timeDiff === 0) {
        taskItem.classList.add("bg-orange"); // היום
      } else if (timeDiff === oneDay) {
        taskItem.classList.add("bg-yellow"); // מחר
      } else {
        taskItem.classList.add("bg-blue"); // עתידי
      }
    
      taskElement.querySelector(".due-date").textContent = `תאריך יעד: ${dueDate.toLocaleDateString('he-IL')}`;
    } else {
      taskElement.querySelector(".due-date").style.display = "none";
    }
    
    // 🧠 קטגוריה וזמן מוערך
    if (task.category || task.time_estimate) {
      const detailsWrapper = document.createElement("div");
      detailsWrapper.classList.add("task-details");
    
      const title = document.createElement("div");
      title.classList.add("task-details-title");
      title.innerHTML = "נוצר אוטומטית באמצעות AI<br><small>ניתן לעדכן בלחיצה על \"ערוך\"</small>";
      detailsWrapper.appendChild(title);
    
      const tagsRow = document.createElement("div");
      tagsRow.classList.add("task-details-row");
    
      if (task.category) {
        const categoryTag = document.createElement("span");
        categoryTag.classList.add("tag", "tag-category");
        categoryTag.textContent = `קטגוריה: ${task.category}`;
        tagsRow.appendChild(categoryTag);
      }
    
      if (task.time_estimate) {
        const timeTag = document.createElement("span");
        timeTag.classList.add("tag", "tag-time");
        timeTag.textContent = `הערכת זמן: ${task.time_estimate}`;
        tagsRow.appendChild(timeTag);
      }
    
      detailsWrapper.appendChild(tagsRow);
    
      const actions = taskElement.querySelector(".task-actions");
      taskItem.insertBefore(detailsWrapper, actions);
    }

    taskElement.querySelector(".edit-btn").addEventListener("click", () => {
      openEditModal(task);
    });

    taskElement.querySelector(".delete-btn").addEventListener("click", () => {
      confirmDeleteTask(task._id);
    });

    tasksList.appendChild(taskElement);
  });
}



// המרת קוד סטטוס לטקסט בעברית
function getStatusText(status) {
  const statusMap = {
    "open": "פתוח",
    "in-progress": "בביצוע",
    "completed": "הושלם"
  };
  return statusMap[status] || status;
}

// פתיחת מודאל להוספת משימה חדשה
function openAddModal() {
  document.getElementById("modalTitle").textContent = "הוספת משימה חדשה";
  document.getElementById("taskForm").reset();
  document.getElementById("taskId").value = "";
  document.getElementById("taskModal").style.display = "block";

  // 🧠 קריאה מיידית ל-AI גם אם התיאור ריק
  const description = document.getElementById("description").value.trim() || "משימה כללית";

  const token = localStorage.getItem("token");

  fetch("/ai/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({ description })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("category").value = data.category || "";
      document.getElementById("timeEstimate").value = data.time_estimate || "";
    })
    .catch(() => {
      document.getElementById("category").value = "";
      document.getElementById("timeEstimate").value = "";
    });
}

// פתיחת מודאל לעריכת משימה קיימת
function openEditModal(task) {
  document.getElementById("modalTitle").textContent = "עריכת משימה";
  document.getElementById("taskId").value = task._id;
  document.getElementById("title").value = task.title;
  document.getElementById("description").value = task.description || "";

  if (task.due_date) {
    const dueDate = new Date(task.due_date);
    const formattedDate = dueDate.toISOString().split('T')[0];
    document.getElementById("dueDate").value = formattedDate;
  } else {
    document.getElementById("dueDate").value = "";
  }

  document.getElementById("status").value = task.status;
  document.getElementById("category").value = task.category || "";
  document.getElementById("timeEstimate").value = task.time_estimate || "";

  document.getElementById("taskModal").style.display = "block";
}


// שמירת משימה (הוספה או עדכון)
async function saveTask(event) {
  event.preventDefault();
  const token = checkAuth();
  const taskId = document.getElementById("taskId").value;

  const taskData = {
    title: document.getElementById("title").value,
    description: document.getElementById("description").value,
    status: document.getElementById("status").value,
    category: document.getElementById("category").value,
    time_estimate: document.getElementById("timeEstimate").value
  };

  const dueDateValue = document.getElementById("dueDate").value;
  if (dueDateValue) {
    taskData.due_date = new Date(dueDateValue).toISOString();
  }

  try {
    const method = taskId ? "PUT" : "POST";
    const url = taskId ? `/api/tasks/${taskId}` : "/api/tasks/";

    const res = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`,
      },
      body: JSON.stringify(taskData),
    });

    if (!res.ok) {
      throw new Error("Failed to save task");
    }

    document.getElementById("taskModal").style.display = "none";
    showMessage(taskId ? "המשימה עודכנה בהצלחה" : "המשימה נוספה בהצלחה", "success");
    getTasks();

  } catch (error) {
    showMessage("שגיאה בשמירת המשימה: " + error.message, "error");
  }
}

// אישור ומחיקת משימה
function confirmDeleteTask(taskId) {
  if (confirm("האם אתה בטוח שברצונך למחוק את המשימה?")) {
    deleteTask(taskId);
  }
}

// מחיקת משימה
async function deleteTask(taskId) {
  const token = checkAuth();
  try {
    const res = await fetch(`/api/tasks/${taskId}`, {
      method: "DELETE",
      headers: {
        "Authorization": `Bearer ${token}`,
      },
    });

    if (!res.ok) {
      throw new Error("Failed to delete task");
    }

    showMessage("המשימה נמחקה בהצלחה", "success");
    getTasks();

  } catch (error) {
    showMessage("שגיאה במחיקת המשימה: " + error.message, "error");
  }
}

// הצגת הודעה למשתמש
function showMessage(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = "toast";
  if (type === "success") toast.style.backgroundColor = "#2ecc71";
  if (type === "error") toast.style.backgroundColor = "#e74c3c";
  toast.textContent = message;

  document.body.appendChild(toast);

  // הוספת המחלקה שמציגה את ההודעה
  setTimeout(() => toast.classList.add("show"), 10);

  // הסתרה אוטומטית אחרי 3 שניות
  setTimeout(() => {
    toast.classList.remove("show");
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}


// התנתקות
function logout() {
  localStorage.removeItem("token");
  window.location.href = "/";
}

async function fetchTelegramCode() {
  const token = localStorage.getItem("token");

  try {
    const res = await fetch("/api/auth/telegram-code", {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();

    if (data.status === "connected") {
      showMessage("כבר מחובר לטלגרם 🎉");
      return;
    }

    if (data.telegram_verification_code) {
      showTelegramPopup(data.telegram_verification_code);
    } else {
      showMessage("לא נמצא קוד טלגרם 🤔");
    }

  } catch (error) {
    showMessage("שגיאה בעת שליפת קוד טלגרם 🚫", "error");
    console.error(error);
  }
}


function showTelegramPopup(telegramCode) {
  const popup = document.createElement("div");
  popup.className = "popup-success";

  popup.innerHTML = `
    <h3>🤖 קישור לטלגרם</h3>
    <p>כדי להתחבר לבוט:</p>
    <ol>
      <li>לחץ/י <a href="https://web.telegram.org/k/#@ShirsTaskBot" target="_blank">כאן</a></li>
      <li>שלח/י את המילה <code>START</code></li>
      <li>שלח/י את הקוד: <strong style="direction:ltr">${telegramCode}</strong></li>
    </ol>
    <div style="margin-top: 20px;">
      <button class="copy-btn" onclick="copyToClipboard(this, '${telegramCode}')">📋 העתק קוד</button>
      <button class="close-popup">✖ סגור</button>
    </div>
  `;

  document.body.appendChild(popup);

  popup.querySelector(".close-popup").addEventListener("click", () => {
    popup.remove();
  });
}




// אירועים
document.addEventListener("DOMContentLoaded", () => {
  getTasks();
  document.getElementById("recommendationBtn").addEventListener("click", () => {
    window.location.href = "/recommendation";
  });
  document.getElementById("addTaskBtn").addEventListener("click", openAddModal);
  document.getElementById("logoutBtn").addEventListener("click", logout);
  document.getElementById("statusFilter").addEventListener("change", getTasks);
  document.getElementById("showTelegramCodeBtn").addEventListener("click", fetchTelegramCode);


  document.getElementById("taskForm").addEventListener("submit", saveTask);
  document.querySelector(".close-modal").addEventListener("click", () => {
    document.getElementById("taskModal").style.display = "none";
  });
  document.querySelector(".cancel-btn").addEventListener("click", () => {
    document.getElementById("taskModal").style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === document.getElementById("taskModal")) {
      document.getElementById("taskModal").style.display = "none";
    }
  });

  // 🧠 קריאה ל-AI בזמן הקלדה בתיאור
  document.getElementById("description").addEventListener("input", async (event) => {
    const description = event.target.value.trim();
    if (!description) return;

    try {
      const res = await fetch("/ai/recommend", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ description })
      });

      if (res.ok) {
        const data = await res.json();
        document.getElementById("category").value = data.category || "";
        document.getElementById("timeEstimate").value = data.time_estimate || "";
      } else {
        document.getElementById("category").value = "";
        document.getElementById("timeEstimate").value = "";
      }
    } catch (error) {
      document.getElementById("category").value = "";
      document.getElementById("timeEstimate").value = "";
    }
  });
});

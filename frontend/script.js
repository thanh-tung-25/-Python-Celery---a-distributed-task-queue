// ==== Chuyển tab giữa sidebar ====
document.querySelectorAll(".sidebar li").forEach((li) => {
  li.addEventListener("click", () => {
    document
      .querySelectorAll(".sidebar li")
      .forEach((i) => i.classList.remove("active"));
    li.classList.add("active");

    document
      .querySelectorAll(".tab")
      .forEach((tab) => tab.classList.remove("active"));
    document.getElementById(li.dataset.tab).classList.add("active");
  });
});

// ==== Gửi email ====
const form = document.getElementById("emailForm");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const subject = document.getElementById("subject").value.trim();
  const content = document.getElementById("content").value.trim();
  const recipients = document
    .getElementById("recipients")
    .value.split("\n")
    .map((r) => r.trim())
    .filter((r) => r);

  if (!recipients.length) return alert("Vui lòng nhập ít nhất 1 email!");

  document.getElementById("statusBox").style.display = "block";
  document.getElementById("status").textContent = "⏳ Đang gửi...";

  try {
    const res = await fetch("/send-email", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subject, content, recipients }),
    });

    const data = await res.json();
    if (res.ok) {
      document.getElementById(
        "status"
      ).textContent = `✅ Task đã gửi lên Celery!\nTask ID: ${data.task_id}`;
    } else {
      document.getElementById("status").textContent = `❌ Lỗi: ${
        data.error || "Không rõ"
      }`;
    }
  } catch (err) {
    document.getElementById("status").textContent =
      "❌ Gửi thất bại: " + err.message;
  }
});

// ==== Lấy lịch sử gửi ====
async function loadLogs() {
  const tbody = document.querySelector("#logsTable tbody");
  tbody.innerHTML = "<tr><td colspan='5'>⏳ Đang tải...</td></tr>";

  try {
    const res = await fetch("/logs");
    const logs = await res.json();

    tbody.innerHTML = "";
    if (!logs.length) {
      tbody.innerHTML = "<tr><td colspan='5'>Chưa có dữ liệu</td></tr>";
      return;
    }

    logs.forEach((log) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${log.id}</td>
        <td>${log.email}</td>
        <td>${log.subject}</td>
        <td>${log.status}</td>
        <td>${log.timestamp}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan='5'>❌ Lỗi tải log: ${err.message}</td></tr>`;
  }
}

document.getElementById("refreshLogs").addEventListener("click", loadLogs);

// Tải sẵn khi mở tab “Lịch sử”
document
  .querySelector('[data-tab="logs-tab"]')
  .addEventListener("click", loadLogs);

// frontend/script.js
const API = "http://127.0.0.1:5000";

document.getElementById("emailForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const to = document.getElementById("to").value;
  const subject = document.getElementById("subject").value;
  const message = document.getElementById("message").value;
  const statusEl = document.getElementById("status");

  statusEl.textContent = "📤 Gửi tác vụ...";

  const res = await fetch(`${API}/send_email`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({to, subject, message})
  });

  if (!res.ok) {
    const err = await res.json();
    statusEl.textContent = "❌ Lỗi: " + (err.error || res.statusText);
    return;
  }

  const data = await res.json();
  const taskId = data.task_id;
  statusEl.textContent = `⏳ Đã xếp hàng (task id: ${taskId}). Đang chờ worker...`;

  // poll for result
  const poll = setInterval(async () => {
    const r = await fetch(`${API}/result/${taskId}`);
    const rr = await r.json();
    if (rr.status === "SUCCESS") {
      clearInterval(poll);
      statusEl.textContent = `✅ Hoàn thành: ${rr.result}`;
    } else if (rr.status === "FAILURE") {
      clearInterval(poll);
      statusEl.textContent = `❌ Thất bại: ${rr.result}`;
    } else {
      // still pending
      statusEl.textContent = `⏳ Trạng thái: ${rr.status} (task id: ${taskId})`;
    }
  }, 1500);
});

// gửi email (list)
document.getElementById("emailForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const subject = document.getElementById("subject").value.trim();
  const content = document.getElementById("content").value.trim();
  const recipients = document.getElementById("recipients").value
    .split("\n").map(s => s.trim()).filter(Boolean);

  if (!recipients.length) { alert("Nhập ít nhất 1 email"); return; }

  const res = await fetch("/send-email", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ subject, content, recipients })
  });

  const data = await res.json();
  if (!res.ok) {
    alert("Server lỗi: " + JSON.stringify(data));
    return;
  }

  document.getElementById("statusBox").style.display = "block";
  document.getElementById("status").textContent = "Task queued: " + data.task_id + "\nĐang gửi...";

  // polling
  const interval = setInterval(async () => {
    const r = await fetch("/result/" + data.task_id);
    const j = await r.json();
    document.getElementById("status").textContent = JSON.stringify(j, null, 2);
    if (j.status === "SUCCESS" || j.status === "FAILURE") {
      clearInterval(interval);
    }
  }, 2000);
});
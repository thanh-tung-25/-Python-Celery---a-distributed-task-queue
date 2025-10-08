const API_BASE = "http://localhost:5000";

async function postJson(url, data) {
  const res = await fetch(url, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });
  return await res.json();
}

async function getJson(url) {
  const res = await fetch(url);
  return await res.json();
}

document.getElementById("sendAdd").addEventListener("click", async () => {
  const a = document.getElementById("a").value || 0;
  const b = document.getElementById("b").value || 0;
  const resp = await postJson(`${API_BASE}/add`, {a: parseInt(a), b: parseInt(b)});
  const id = resp.task_id;
  document.getElementById("addStatus").textContent = `Task gửi: ${id} — Đang chờ...`;
  pollResult(id, (data) => {
    document.getElementById("addStatus").textContent = `Kết quả: ${data.result} (status: ${data.status})`;
  });
});

document.getElementById("sendReverse").addEventListener("click", async () => {
  const text = document.getElementById("text").value || "";
  const resp = await postJson(`${API_BASE}/add`, {a: 0, b: 0}); // not used; use separate endpoint if needed
  // For demo, call reverse via task name endpoint - create new endpoint in API if wanted.
  alert("Sử dụng demo: vui lòng dùng endpoint /add cho phép cộng. Bạn có thể mở rộng API để gọi reverse_text.");
});

function pollResult(taskId, callback) {
  const iv = setInterval(async () => {
    const data = await getJson(`${API_BASE}/result/${taskId}`);
    if (data.status === "SUCCESS" || data.status === "FAILURE") {
      clearInterval(iv);
      callback(data);
    }
  }, 1000);
}

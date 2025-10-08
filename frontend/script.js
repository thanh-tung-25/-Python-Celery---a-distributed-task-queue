async function sendTask() {
  const a = document.getElementById("a").value;
  const b = document.getElementById("b").value;
  
  const response = await fetch("http://localhost:5000/add", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ a: parseInt(a), b: parseInt(b) })
  });

  const data = await response.json();
  document.getElementById("result").textContent = "📤 Đang xử lý... Mã task: " + data.task_id;

  // Poll kết quả
  checkResult(data.task_id);
}

async function checkResult(taskId) {
  const interval = setInterval(async () => {
    const res = await fetch(`http://localhost:5000/result/${taskId}`);
    const data = await res.json();
    if (data.status === "SUCCESS") {
      clearInterval(interval);
      document.getElementById("result").textContent = "✅ Kết quả: " + data.result;
    }
  }, 1000);
}

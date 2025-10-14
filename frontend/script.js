// frontend/script.js
// ---------------------------------------------------------
// Frontend logic for Celery email demo (SIMULATED mode)
// Features:
// - Send email task to API (/send-email)
// - Poll /result/<task_id> until SUCCESS/FAILURE
// - Show live status, progress spinner
// - Maintain history in localStorage with timestamps
// - Retry/polling management and graceful error handling
// ---------------------------------------------------------

(() => {
  // Config
  const API_BASE = "http://127.0.0.1:5000"; // backend API
  const POLL_INTERVAL = 1500; // ms
  const HISTORY_KEY = "email_task_history_v1";

  // Elements
  const sendBtn = document.getElementById("sendBtn");
  const clearBtn = document.getElementById("clearBtn");
  const toEl = document.getElementById("to");
  const subjectEl = document.getElementById("subject");
  const messageEl = document.getElementById("message");
  const priorityEl = document.getElementById("priority");
  const liveStatus = document.getElementById("liveStatus");
  const statusText = document.getElementById("statusText");
  const historyList = document.getElementById("historyList");
  const clearHistoryBtn = document.getElementById("clearHistory");
  const refreshAllBtn = document.getElementById("refreshAll");
  const resultEl = document.getElementById("result");

  // Utils
  function nowISO() { return new Date().toISOString(); }
  function formatShort(ts) {
    try {
      const d = new Date(ts);
      return d.toLocaleString();
    } catch { return ts; }
  }
  function validateEmail(email) {
    if (!email) return false;
    // simple email regex
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // Local storage for history
  function loadHistory() {
    const raw = localStorage.getItem(HISTORY_KEY);
    if (!raw) return [];
    try { return JSON.parse(raw) || []; } catch { return []; }
  }
  function saveHistory(arr) {
    try { localStorage.setItem(HISTORY_KEY, JSON.stringify(arr)); } catch (e) { console.warn("Unable to save history", e); }
  }
  function addHistoryItem(item) {
    const arr = loadHistory();
    arr.unshift(item); // newest first
    // keep max 100 entries
    if (arr.length > 100) arr.length = 100;
    saveHistory(arr);
    renderHistory();
  }

  // Render history list
  function renderHistory() {
    const arr = loadHistory();
    historyList.innerHTML = "";
    if (arr.length === 0) {
      historyList.innerHTML = `<div class="muted">Chưa có task nào — gửi thử một email để demo.</div>`;
      return;
    }
    for (const h of arr) {
      const node = document.createElement("div");
      node.className = "history-item";
      node.innerHTML = `
        <div class="history-left">
          <div style="font-weight:700">${escapeHTML(h.to)}</div>
          <div class="history-meta">${escapeHTML(h.subject)} • ${formatShort(h.created_at)}</div>
          <div style="margin-top:8px;font-size:13px" id="history-res-${h.task_id}">${h.status === "PENDING" ? "<span class='muted'>Đang chờ...</span>" : formatStatus(h)}</div>
        </div>
        <div class="history-actions">
          <div style="text-align:right;">
            <div class="history-meta">ID: <span style="font-family:monospace;font-size:12px">${h.task_id.slice(0,8)}</span></div>
            <div style="margin-top:8px;">
              <button class="btn btn--ghost" data-action="refresh" data-id="${h.task_id}">Cập nhật</button>
              <button class="btn btn--ghost" data-action="view" data-id="${h.task_id}">Xem</button>
            </div>
          </div>
        </div>
      `;
      historyList.appendChild(node);
    }
  }

  function formatStatus(h) {
    if (h.status === "SUCCESS") return `<span class="success">Hoàn tất</span> — ${escapeHTML(h.result || "")}`;
    if (h.status === "FAILURE") return `<span class="error">Thất bại</span> — ${escapeHTML(h.result || "")}`;
    return `<span class="muted">${escapeHTML(h.status)}</span>`;
  }

  // Basic escaping
  function escapeHTML(s) {
    if (!s && s !== 0) return "";
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  // UI helpers
  function setSending(isSending, text = "Đang gửi...") {
    if (isSending) {
      liveStatus.style.display = "flex";
      statusText.textContent = text;
      sendBtn.disabled = true;
    } else {
      liveStatus.style.display = "none";
      sendBtn.disabled = false;
    }
  }

  // API calls
  async function apiSendEmail(payload) {
    const url = `${API_BASE}/send-email`;
    const res = await fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API lỗi ${res.status}: ${txt}`);
    }
    return res.json();
  }

  async function apiGetResult(taskId) {
    const url = `${API_BASE}/result/${taskId}`;
    const res = await fetch(url);
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`API lỗi ${res.status}: ${txt}`);
    }
    return res.json();
  }

  // Polling logic
  function pollTask(taskId, onUpdate, onFinish) {
    let stopped = false;
    const iv = setInterval(async () => {
      if (stopped) return clearInterval(iv);
      try {
        const r = await apiGetResult(taskId);
        // r.status could be "PENDING", "SUCCESS", "FAILURE", or celery states
        onUpdate && onUpdate(r);
        if (r.status === "SUCCESS" || r.status === "FAILURE") {
          stopped = true;
          clearInterval(iv);
          onFinish && onFinish(r);
        }
      } catch (err) {
        console.error("Polling error:", err);
        // don't stop on network error, just report
        onUpdate && onUpdate({status: "ERROR", result: err.message});
      }
    }, POLL_INTERVAL);
    return () => { stopped = true; clearInterval(iv); };
  }

  // Send handler
  async function handleSend() {
    const to = toEl.value.trim();
    const subject = subjectEl.value.trim();
    const message = messageEl.value.trim();
    const priority = priorityEl.value;

    if (!validateEmail(to)) {
      alert("Vui lòng nhập địa chỉ email hợp lệ.");
      toEl.focus();
      return;
    }
    if (!subject || !message) {
      alert("Tiêu đề và nội dung không được để trống.");
      return;
    }

    const payload = { to, subject, message, priority };

    try {
      setSending(true, "📤 Đang gửi task...");
      const json = await apiSendEmail(payload);
      const taskId = json.task_id || json.id || null;
      if (!taskId) throw new Error("Không nhận được task_id từ server.");

      // Add to history as PENDING
      const hist = { task_id: taskId, to, subject, message, priority, status: "PENDING", created_at: nowISO(), result: null };
      addHistoryItem(hist);

      // Start polling
      const stop = pollTask(taskId,
        (r) => { // onUpdate
          // update history item status display
          updateHistoryItem(taskId, r);
          // live status text
          statusText.textContent = `⏳ Trạng thái: ${r.status}`;
        },
        (r) => { // onFinish
          setSending(false);
          statusText.textContent = r.status === "SUCCESS" ? "✅ Hoàn thành" : "❌ Thất bại";
          // update history final
          updateHistoryItem(taskId, r, true);
          // show brief toast (simple)
          flashMessage(r.status === "SUCCESS" ? "Gửi email hoàn tất." : "Gửi email thất bại.", r.status === "SUCCESS");
        }
      );

    } catch (err) {
      console.error("Send error:", err);
      setSending(false);
      flashMessage("Lỗi khi gửi task: " + err.message, false);
    }
  }

  // Update single history entry in storage and re-render
  function updateHistoryItem(taskId, r, finalize = false) {
    const arr = loadHistory();
    const idx = arr.findIndex(x => x.task_id === taskId);
    if (idx === -1) return;
    arr[idx].status = r.status || arr[idx].status;
    if (r.result !== undefined) arr[idx].result = r.result;
    if (finalize) arr[idx].finished_at = nowISO();
    saveHistory(arr);
    renderHistory();
  }

  // Flash short message
  function flashMessage(text, ok = true) {
    const tmp = document.createElement("div");
    tmp.style.position = "fixed";
    tmp.style.right = "18px";
    tmp.style.bottom = "18px";
    tmp.style.padding = "12px 16px";
    tmp.style.borderRadius = "10px";
    tmp.style.background = ok ? "rgba(22,163,74,0.95)" : "rgba(220,38,38,0.95)";
    tmp.style.color = "#fff";
    tmp.style.boxShadow = "0 8px 24px rgba(2,6,23,0.2)";
    tmp.style.zIndex = 9999;
    tmp.textContent = text;
    document.body.appendChild(tmp);
    setTimeout(()=>{ tmp.style.transition="opacity 300ms"; tmp.style.opacity=0; setTimeout(()=>tmp.remove(),350); }, 2600);
  }

  // Event wiring
  sendBtn.addEventListener("click", handleSend);
  clearBtn.addEventListener("click", () => {
    toEl.value = ""; subjectEl.value = ""; messageEl.value = ""; priorityEl.value = "normal";
  });
  clearHistoryBtn.addEventListener("click", () => {
    if (!confirm("Bạn có chắc muốn xóa lịch sử (không thể hoàn tác)?")) return;
    localStorage.removeItem(HISTORY_KEY);
    renderHistory();
  });
  refreshAllBtn.addEventListener("click", () => {
    // go through all pending tasks and trigger an update
    const arr = loadHistory();
    for (const h of arr.filter(x => x.status === "PENDING")) {
      pollTask(h.task_id, r => updateHistoryItem(h.task_id, r), r => updateHistoryItem(h.task_id, r, true));
    }
  });

  // click handlers for history buttons (delegate)
  historyList.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn) return;
    const action = btn.dataset.action;
    const id = btn.dataset.id;
    if (action === "refresh") {
      // manual refresh one
      pollTask(id, r => updateHistoryItem(id, r), r => updateHistoryItem(id, r, true));
      flashMessage("Đang cập nhật task...", true);
    } else if (action === "view") {
      // show details
      const arr = loadHistory();
      const h = arr.find(x => x.task_id === id);
      if (!h) return alert(`Không tìm thấy task ${id}`);
      alert(`Task ID: ${h.task_id}\nTo: ${h.to}\nSubject: ${h.subject}\nStatus: ${h.status}\nResult: ${h.result || "(chưa có)"}`);
    }
  });

  // init
  function init() {
    renderHistory();
    // try to focus first input
    try { toEl.focus(); } catch {}
  }

  // run init on DOMContentLoaded
  document.addEventListener("DOMContentLoaded", init);

})();

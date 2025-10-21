const form = document.getElementById('emailForm');
const status = document.getElementById('status');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        recipient: form.recipient.value,
        subject: form.subject.value,
        body: form.body.value
    };
    status.textContent = "Sending...";
    const res = await fetch('/send_email', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    status.textContent = `Task queued. Task ID: ${result.task_id}`;
});

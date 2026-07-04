const API_BASE = 'http://localhost:8000';

let allTickets = [];

// Tab switching
function showTab(tab) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    document.getElementById(`${tab}-tab`).classList.add('active');
    document.querySelector(`[onclick="showTab('${tab}')"]`).classList.add('active');
    if (tab === 'dashboard') loadTickets();
}

// Submit ticket form
document.getElementById('ticketForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    const msgEl = document.getElementById('submitMessage');

    btn.disabled = true;
    btn.querySelector('.btn-text').textContent = 'Submitting...';
    btn.querySelector('.spinner').style.display = 'inline';
    msgEl.style.display = 'none';

    const payload = {
        title: document.getElementById('title').value.trim(),
        description: document.getElementById('description').value.trim(),
        submitter_name: document.getElementById('submitter_name').value.trim(),
        submitter_email: document.getElementById('submitter_email').value.trim(),
    };
    const category = document.getElementById('category').value;
    const priority = document.getElementById('priority').value;
    if (category) payload.category = category;
    if (priority) payload.priority = priority;

    try {
        const res = await fetch(`${API_BASE}/tickets`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Failed to submit ticket');

        msgEl.className = 'message success';
        msgEl.innerHTML = `
            <strong>✅ Ticket submitted successfully!</strong><br>
            Ticket ID: <code>${data.id}</code><br>
            AI detected: <strong>${data.category}</strong> | Priority: <strong>${data.priority}</strong>
        `;
        msgEl.style.display = 'block';
        document.getElementById('ticketForm').reset();
    } catch (err) {
        msgEl.className = 'message error';
        msgEl.textContent = `❌ ${err.message}`;
        msgEl.style.display = 'block';
    } finally {
        btn.disabled = false;
        btn.querySelector('.btn-text').textContent = 'Submit Ticket';
        btn.querySelector('.spinner').style.display = 'none';
    }
});

// Load tickets from API
async function loadTickets() {
    const container = document.getElementById('ticketsContainer');
    container.innerHTML = '<div class="loading">⏳ Loading tickets...</div>';

    try {
        const email = document.getElementById('searchEmail').value.trim();
        const status = document.getElementById('statusFilter').value;
        const params = new URLSearchParams();
        if (email) params.append('submitter_email', email);
        if (status) params.append('status', status);

        const res = await fetch(`${API_BASE}/tickets?${params.toString()}`);
        if (!res.ok) throw new Error('Failed to fetch tickets');
        const data = await res.json();
        allTickets = Array.isArray(data) ? data : (data.tickets || []);
        renderTickets(allTickets);
    } catch (err) {
        container.innerHTML = `<div class="message error">❌ ${err.message}. Make sure the backend is running on port 8000.</div>`;
    }
}

// Filter tickets without re-fetching
function filterTickets() {
    clearTimeout(window._filterTimer);
    window._filterTimer = setTimeout(loadTickets, 400);
}

// Render ticket list
function renderTickets(tickets) {
    const container = document.getElementById('ticketsContainer');
    if (!tickets.length) {
        container.innerHTML = '<div class="loading">No tickets found.</div>';
        return;
    }

    container.innerHTML = tickets.map(t => `
        <div class="ticket-item" onclick="openTicket('${t.id || t._id}')">
            <div class="ticket-header">
                <div>
                    <div class="ticket-title">${escapeHtml(t.title)}</div>
                    <div class="ticket-meta">
                        <span>👤 ${escapeHtml(t.submitter_name)}</span>
                        <span>✉️ ${escapeHtml(t.submitter_email)}</span>
                        <span>🕒 ${formatDate(t.created_at)}</span>
                    </div>
                </div>
                <div style="display:flex;gap:8px;flex-wrap:wrap;">
                    <span class="badge badge-status badge-${t.status}">${t.status}</span>
                    ${t.priority ? `<span class="badge badge-${t.priority}">${t.priority}</span>` : ''}
                    ${t.category ? `<span class="badge badge-${t.category}">${t.category}</span>` : ''}
                </div>
            </div>
            <div class="ticket-description">${escapeHtml(t.description)}</div>
            ${t.ai_analysis?.tags?.length ? `
                <div class="ticket-tags">
                    ${t.ai_analysis.tags.slice(0, 4).map(tag => `<span class="badge" style="background:#f1f5f9;color:#475569;">#${escapeHtml(tag)}</span>`).join('')}
                </div>` : ''}
        </div>
    `).join('');
}

// Open ticket detail modal
async function openTicket(ticketId) {
    const modal = document.getElementById('ticketModal');
    const body = document.getElementById('modalBody');
    modal.style.display = 'block';
    body.innerHTML = '<div class="loading">⏳ Loading ticket details...</div>';

    try {
        const res = await fetch(`${API_BASE}/tickets/${ticketId}`);
        if (!res.ok) throw new Error('Ticket not found');
        const t = await res.json();
        const ai = t.ai_analysis || {};

        body.innerHTML = `
            <h2 style="margin-bottom:5px;">🎫 ${escapeHtml(t.title)}</h2>
            <div style="margin-bottom:20px;display:flex;gap:10px;flex-wrap:wrap;">
                <span class="badge badge-status badge-${t.status}">${t.status}</span>
                ${t.priority ? `<span class="badge badge-${t.priority}">${t.priority}</span>` : ''}
                ${t.category ? `<span class="badge badge-${t.category}">${t.category}</span>` : ''}
            </div>

            <div class="detail-info">
                <div class="info-item">
                    <div class="info-label">Submitted by</div>
                    <div class="info-value">${escapeHtml(t.submitter_name)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Email</div>
                    <div class="info-value">${escapeHtml(t.submitter_email)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Created</div>
                    <div class="info-value">${formatDate(t.created_at)}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Est. Resolution</div>
                    <div class="info-value">${ai.estimated_resolution_time || 'N/A'}</div>
                </div>
            </div>

            <div class="detail-section">
                <h3>📋 Description</h3>
                <p style="color: var(--text-secondary); white-space: pre-wrap;">${escapeHtml(t.description)}</p>
            </div>

            ${ai.summary ? `
            <div class="detail-section">
                <h3>🤖 AI Analysis</h3>
                <div class="ai-analysis">
                    <h4>Summary</h4>
                    <p>${escapeHtml(ai.summary)}</p>
                    ${ai.reasoning ? `<p style="opacity:0.8;margin-top:8px;font-size:0.9rem;">${escapeHtml(ai.reasoning)}</p>` : ''}
                    ${ai.confidence ? `
                        <p style="margin-top:10px;font-size:0.85rem;">Confidence: ${Math.round(ai.confidence * 100)}%</p>
                        <div class="confidence-bar"><div class="confidence-fill" style="width:${ai.confidence * 100}%"></div></div>
                    ` : ''}
                </div>
            </div>` : ''}

            ${ai.suggested_response ? `
            <div class="detail-section">
                <h3>💬 Suggested Response</h3>
                <div style="padding:15px;background:var(--bg-color);border-radius:8px;border-left:4px solid var(--primary-color);">
                    <p style="color:var(--text-secondary);white-space:pre-wrap;">${escapeHtml(ai.suggested_response)}</p>
                </div>
            </div>` : ''}

            ${ai.tags?.length ? `
            <div class="detail-section">
                <h3>🏷️ Tags</h3>
                <div class="ticket-tags">
                    ${ai.tags.map(tag => `<span class="badge" style="background:#f1f5f9;color:#475569;">#${escapeHtml(tag)}</span>`).join('')}
                </div>
            </div>` : ''}

            <div class="detail-section" style="margin-top:25px;">
                <h3>Update Status</h3>
                <div style="display:flex;gap:10px;flex-wrap:wrap;">
                    ${['OPEN','IN_PROGRESS','RESOLVED','CLOSED'].map(s => `
                        <button class="btn ${t.status === s ? 'btn-primary' : 'btn-secondary'}"
                                onclick="updateStatus('${t.id || t._id}', '${s}')"
                                style="${t.status === s ? '' : 'background:#94a3b8;'}">
                            ${s.replace('_',' ')}
                        </button>
                    `).join('')}
                </div>
            </div>
        `;
    } catch (err) {
        body.innerHTML = `<div class="message error">❌ ${err.message}</div>`;
    }
}

// Update ticket status
async function updateStatus(ticketId, status) {
    try {
        const res = await fetch(`${API_BASE}/tickets/${ticketId}/status`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status }),
        });
        if (!res.ok) throw new Error('Failed to update status');
        await openTicket(ticketId);
        loadTickets();
    } catch (err) {
        alert(`Error: ${err.message}`);
    }
}

// Close modal
function closeModal() {
    document.getElementById('ticketModal').style.display = 'none';
}

window.onclick = (e) => {
    if (e.target === document.getElementById('ticketModal')) closeModal();
};

// Utility helpers
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleString();
}

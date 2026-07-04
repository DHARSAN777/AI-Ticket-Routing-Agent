// ── Chat State ──────────────────────────────────────────────
const state = {
  name: '',
  issue: '',
  category: '',
  priority: '',
  team: '',
  sentiment: '',
  confidence: 0,
  qCount: 0,       // how many troubleshooting questions asked
  answers: [],     // user answers collected
  phase: 'idle',   // idle | routing | questioning | solving | done
};

// ── Step Tracker ────────────────────────────────────────────
function setStep(n) {
  for (let i = 1; i <= 7; i++) {
    const dot = document.getElementById('dot' + i);
    if (i < n)       { dot.className = 'step-dot done'; dot.textContent = '✓'; }
    else if (i === n){ dot.className = 'step-dot active'; dot.textContent = i; }
    else             { dot.className = 'step-dot';        dot.textContent = i; }
  }
}

// ── Message Renderer ────────────────────────────────────────
function now() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addMsg(role, html, type = '') {
  const wrap = document.getElementById('chatMessages');
  const isUser = role === 'user';
  const div = document.createElement('div');
  div.className = `msg ${isUser ? 'user' : 'bot'}`;
  div.innerHTML = `
    <div class="msg-avatar">${isUser ? '👤' : '🤖'}</div>
    <div class="msg-body">
      <div class="msg-sender">${isUser ? state.name || 'You' : 'AI Agent'}</div>
      <div class="msg-bubble ${type}">${html}</div>
      <div class="msg-time">${now()}</div>
    </div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

function addTyping() {
  const wrap = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = 'msg bot';
  div.id = 'typingMsg';
  div.innerHTML = `<div class="msg-avatar">🤖</div>
    <div class="msg-body">
      <div class="msg-sender">AI Agent</div>
      <div class="typing"><span></span><span></span><span></span></div>
    </div>`;
  wrap.appendChild(div);
  wrap.scrollTop = wrap.scrollHeight;
}

function removeTyping() {
  const t = document.getElementById('typingMsg');
  if (t) t.remove();
}

function setQuickReplies(options) {
  const qr = document.getElementById('quickReplies');
  qr.innerHTML = options.map(o =>
    `<button class="qr-btn" onclick="sendQuick('${o}')">${o}</button>`
  ).join('');
}

function clearQuickReplies() {
  document.getElementById('quickReplies').innerHTML = '';
}

function updatePanel(data) {
  document.getElementById('infoStatus').textContent    = data.status    || 'Active';
  document.getElementById('infoCategory').textContent  = data.category  || '—';
  document.getElementById('infoPriority').textContent  = data.priority  || '—';
  document.getElementById('infoTeam').textContent      = data.team      || '—';
  document.getElementById('infoSentiment').textContent = data.sentiment || '—';
  document.getElementById('infoConfidence').textContent= data.confidence
    ? Math.round(data.confidence * 100) + '%' : '—';
}

// ── Gemini API Call (via backend or direct mock) ─────────────
async function callGemini(prompt) {
  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: prompt, history: [] })
    });
    if (!res.ok) throw new Error('API error');
    const data = await res.json();
    return data.response || data.message || '';
  } catch {
    return null; // fallback to mock
  }
}

// ── STEP 1: Start Chat ───────────────────────────────────────
async function startChat() {
  const issue = document.getElementById('startIssue').value.trim();
  if (!issue) { alert('Please describe your issue first.'); return; }

  // Use generic customer reference
  state.name  = 'Customer';
  state.issue = issue;
  state.phase = 'routing';

  // Switch to chat view
  document.getElementById('startForm').style.display = 'none';
  const ca = document.getElementById('chatArea');
  ca.style.display = 'flex';
  ca.style.flexDirection = 'column';

  setStep(1);
  addMsg('user', escHtml(issue));
  setStep(2);

  // Show typing, then route
  await delay(600);
  addTyping();
  await delay(1400);
  removeTyping();

  // ── STEP 2: Routing Agent ──
  await routeTicket(issue);
}

// ── STEP 2: Ticket Routing ───────────────────────────────────
async function routeTicket(issue) {
  setStep(2);

  // Try real API first, fallback to mock
  let routing = await fetchRouting(issue);
  if (!routing) routing = mockRouting(issue);

  state.category   = routing.category;
  state.priority   = routing.priority;
  state.team       = routing.assigned_team;
  state.sentiment  = routing.sentiment;
  state.confidence = routing.confidence_score;

  updatePanel({
    status: 'Routing...', category: routing.category,
    priority: routing.priority, team: routing.assigned_team,
    sentiment: routing.sentiment, confidence: routing.confidence_score
  });

  setStep(3);

  // Show routing result bubble
  const priColor = { Critical:'#ef4444', High:'#fb923c', Medium:'#fbbf24', Low:'#34d399' }[routing.priority] || '#a5b4fc';
  addMsg('bot', `
    <strong>🎯 Ticket Routed Successfully</strong>
    <div class="routing-grid">
      <div class="routing-item"><div class="routing-item-label">Category</div><div class="routing-item-val">${routing.category}</div></div>
      <div class="routing-item"><div class="routing-item-label">Priority</div><div class="routing-item-val" style="color:${priColor}">${routing.priority}</div></div>
      <div class="routing-item"><div class="routing-item-label">Assigned Team</div><div class="routing-item-val">${routing.assigned_team}</div></div>
      <div class="routing-item"><div class="routing-item-label">Sentiment</div><div class="routing-item-val">${routing.sentiment}</div></div>
    </div>
    <div style="margin-top:10px;padding:10px;background:var(--bg);border-radius:8px;font-size:0.85rem;color:var(--text2);">
      📋 ${routing.summary}
    </div>
  `, 'routing');

  await delay(800);
  setStep(4);

  // ── STEP 3: Troubleshooting Agent intro ──
  addTyping();
  await delay(1200);
  removeTyping();
  addMsg('bot', `Hi there! 👋 I'm the <strong>Troubleshooting Agent</strong> for the <strong>${routing.category}</strong> team.<br><br>
    I'm going to ask you <strong>2–3 quick questions</strong> so I can give you an accurate solution. Let's get this sorted! 🔧`);

  await delay(800);
  state.phase = 'questioning';
  state.qCount = 0;
  state.answers = [];

  await askQuestion(1);
}

// ── STEP 3: Ask Diagnostic Questions ────────────────────────
const QUESTIONS = {
  'Billing': [
    { q: 'Was the payment processed through credit card, debit card, or another method?', opts: ['Credit Card', 'Debit Card', 'PayPal', 'Other'] },
    { q: 'Did you receive a payment confirmation email or receipt?', opts: ['Yes, I received it', 'No email received', 'Email went to spam'] },
    { q: 'Has this payment issue happened before on your account?', opts: ['First time', 'Happened before', 'Happens regularly'] },
  ],
  'Login Issue': [
    { q: 'What error message are you seeing when you try to log in?', opts: ['Invalid password', 'Account locked', 'Authentication failed', 'Page not loading'] },
    { q: 'When did you last successfully log in?', opts: ['Today', 'Yesterday', 'Last week', 'Never worked'] },
    { q: 'Have you tried resetting your password?', opts: ['Yes, but still failing', 'No, not yet', 'Reset email not arriving'] },
  ],
  'Technical Support': [
    { q: 'Which browser or device are you using?', opts: ['Chrome', 'Firefox', 'Safari', 'Mobile App'] },
    { q: 'When did this issue start occurring?', opts: ['Just now', 'Today', 'After an update', 'Last few days'] },
    { q: 'Does the issue happen every time or intermittently?', opts: ['Every time', 'Sometimes', 'Only on certain pages'] },
  ],
  'Refund Request': [
    { q: 'How long ago was the original purchase made?', opts: ['Today', 'Within 7 days', 'Within 30 days', 'Over 30 days ago'] },
    { q: 'What is the reason for the refund request?', opts: ['Wrong item received', 'Product defective', 'Duplicate charge', 'Changed my mind'] },
    { q: 'Do you have your order number or transaction ID?', opts: ['Yes, I have it', 'No, I lost it', 'I can find it'] },
  ],
  'Product Bug': [
    { q: 'Can you reproduce the bug consistently?', opts: ['Yes, always happens', 'Sometimes', 'Only once'] },
    { q: 'Which feature or page has the bug?', opts: ['Dashboard', 'Settings', 'Export/Import', 'Other'] },
    { q: 'Have you tried clearing cache or using a different browser?', opts: ['Yes, still happening', 'No, not yet', 'Partially fixed it'] },
  ],
  'Security': [
    { q: 'What suspicious activity did you notice?', opts: ['Unauthorized login', 'Password changed', 'Unknown charges', 'Account data changed'] },
    { q: 'Have you already changed your password?', opts: ['Yes just now', 'No not yet', 'Cannot access account'] },
    { q: 'Do you have two-factor authentication enabled?', opts: ['Yes', 'No', 'Not sure'] },
  ],
};

function getQuestions() {
  const cat = state.category;
  return QUESTIONS[cat] || QUESTIONS['Technical Support'];
}

async function askQuestion(num) {
  setStep(5);
  const questions = getQuestions();
  const idx = num - 1;
  if (idx >= questions.length || idx >= 3) {
    await giveSolution();
    return;
  }

  const q = questions[idx];
  addTyping();
  await delay(900);
  removeTyping();
  addMsg('bot', `<strong>Question ${num} of ${Math.min(questions.length, 3)}:</strong><br><br>${q.q}`);

  if (q.opts) setQuickReplies(q.opts);
  state.qCount = num;
  enableInput();
}

// ── STEP 4: User sends a message ────────────────────────────
function sendMessage() {
  const input = document.getElementById('chatInput');
  const text  = input.value.trim();
  if (!text) return;
  input.value = '';
  clearQuickReplies();
  addMsg('user', escHtml(text));
  handleUserReply(text);
}

function sendQuick(text) {
  clearQuickReplies();
  addMsg('user', escHtml(text));
  handleUserReply(text);
}

async function handleUserReply(text) {
  disableInput();
  state.answers.push(text);

  if (state.phase === 'questioning') {
    if (state.qCount < 3) {
      // Acknowledge and ask next question
      await delay(400);
      addTyping();
      await delay(700);
      removeTyping();
      const acks = ['Got it! 👍', 'Understood.', 'Thanks for that info!', 'Perfect, that helps!'];
      addMsg('bot', acks[Math.floor(Math.random() * acks.length)]);
      await delay(400);
      await askQuestion(state.qCount + 1);
    } else {
      await giveSolution();
    }
  } else if (state.phase === 'done') {
    // Follow-up after solution
    addTyping();
    await delay(1000);
    removeTyping();
    addMsg('bot', `Thank you for the follow-up! If the issue persists, our <strong>${state.team}</strong> team will contact you shortly. 
      <br><br>Is there anything else I can help you with?`);
    setQuickReplies(['Yes, I have another issue', 'No, problem solved! ✅', 'I need to escalate this']);
    enableInput();
  }
}

// ── STEP 5: Give Solution ────────────────────────────────────
const SOLUTIONS = {
  'Billing': {
    steps: [
      '1. Check your email for a payment confirmation receipt.',
      '2. Log in to your account → Billing → Payment History to verify the charge.',
      '3. If double-charged, contact your bank to report the duplicate.',
      '4. We will investigate and issue a refund within 5-7 business days.',
      '5. Enable "Payment Alerts" in Settings to prevent future issues.'
    ],
    reason: 'Payment failures often occur due to expired cards, insufficient funds, or network timeouts that cause duplicate attempts.',
    prevention: 'Keep your payment method updated, enable 2-factor auth, and monitor your account regularly for unusual activity.'
  },
  'Login Issue': {
    steps: [
      '1. Click "Forgot Password?" and enter your registered email.',
      '2. Check your email (and spam folder) for the password reset link.',
      '3. Click the link and create a new password (use a mix of letters, numbers, symbols).',
      '4. Try logging in with your new password.',
      '5. If the reset email doesn\'t arrive, verify your email address in Account Settings.',
      '6. If still failing, disable browser extensions (especially password managers) and try incognito mode.'
    ],
    reason: 'Login failures are typically caused by incorrect credentials, expired sessions, browser cache, or account lockouts after failed attempts.',
    prevention: 'Use a password manager to store complex passwords, enable multi-factor authentication, and log out from untrusted devices.'
  },
  'Technical Support': {
    steps: [
      '1. Clear your browser cache: Settings → Clear Browsing Data → All Time.',
      '2. Try a different browser (Chrome, Firefox, Safari) to isolate the issue.',
      '3. Disable all browser extensions temporarily.',
      '4. Check your internet connection speed (open speedtest.net).',
      '5. If on mobile, uninstall and reinstall the app.',
      '6. Try accessing from a different network (mobile hotspot or another wifi).',
      '7. Restart your device and try again.'
    ],
    reason: 'Technical issues often stem from browser compatibility, cache corruption, network problems, or outdated app versions.',
    prevention: 'Keep your browser updated, clear cache weekly, update apps regularly, and use a stable internet connection.'
  },
  'Refund Request': {
    steps: [
      '1. Locate your order number (check email confirmation or account history).',
      '2. Check the refund policy: items within 30 days get full refund; after 30 days may have restocking fees.',
      '3. If eligible, request refund through Account → Order History → Request Refund.',
      '4. Our Finance team will process within 5-10 business days.',
      '5. Refunds are issued to the original payment method.',
      '6. Contact support if refund doesn\'t appear in 2 weeks.'
    ],
    reason: 'Refund processing requires verification of order status, return eligibility, and authorization.',
    prevention: 'Review product details carefully before purchase, check return policies upfront, and keep order confirmations.'
  },
  'Product Bug': {
    steps: [
      '1. Reproduce the bug: note exact steps and browser/device used.',
      '2. Clear cache and hard-refresh (Ctrl+Shift+R or Cmd+Shift+R).',
      '3. Try the action in incognito/private mode.',
      '4. Take a screenshot or video of the bug.',
      '5. Report it with: browser, OS version, screenshots, and reproduction steps.',
      '6. Our Engineering team will prioritize and deploy a fix.',
      '7. Check release notes for updates.'
    ],
    reason: 'Bugs may be caused by browser incompatibility, cached data, server-side issues, or recent deployments.',
    prevention: 'Keep your browser and OS updated, report bugs immediately with details, and use supported browsers.'
  },
  'Security': {
    steps: [
      '🚨 URGENT: Change your password immediately!',
      '1. Log out from all devices (Account → Active Sessions → Logout All).',
      '2. Change your password to something strong and unique.',
      '3. Enable Multi-Factor Authentication (Settings → Security → 2FA).',
      '4. Review recent login activity (Settings → Login History) and remove unknown sessions.',
      '5. Check for authorized apps/integrations (Settings → Connected Apps).',
      '6. Our Security team will investigate and contact you.',
      '7. Monitor your account closely for the next 30 days.'
    ],
    reason: 'Security breaches are serious and may indicate compromised credentials, malware, or unauthorized access attempts.',
    prevention: 'Use strong unique passwords, enable 2FA, never share credentials, verify emails/links carefully, and report suspicious activity immediately.'
  },
};

async function giveSolution() {
  setStep(6);
  state.phase = 'solving';

  addTyping();
  await delay(1500);
  removeTyping();

  const sol = SOLUTIONS[state.category] || SOLUTIONS['Technical Support'];

  // Solution message
  addMsg('bot', `
    <strong>🔧 Solution for ${state.category}</strong><br><br>
    ${sol.steps.map(s => `<div style="margin:8px 0; line-height: 1.7;">${s}</div>`).join('')}
  `, 'solution');

  await delay(1200);

  // Reason + Prevention
  addMsg('bot', `
    <strong>💡 Why This Happened</strong><br>
    ${sol.reason}<br><br>
    <strong>🛡️ Prevention Tips</strong><br>
    ${sol.prevention}
  `);

  await delay(800);
  setStep(7);
  state.phase = 'done';

  clearQuickReplies();
  addMsg('bot', `
    That's the solution! 🎉 Let me know if this fixed your issue or if you need further assistance.
  `);
  setQuickReplies(['Yes, it worked! ✅', 'Still having issues 😞', 'Need to escalate']);
  enableInput();
}

// ── Helper Functions ────────────────────────────────────────
function escHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function disableInput() {
  document.getElementById('chatInput').disabled = true;
  document.getElementById('sendBtn').disabled = true;
}

function enableInput() {
  document.getElementById('chatInput').disabled = false;
  document.getElementById('sendBtn').disabled = false;
  document.getElementById('chatInput').focus();
}

// ── Fetch Routing from Backend API ───────────────────────────
async function fetchRouting(issue) {
  try {
    const res = await fetch(`${API_BASE || 'http://localhost:8080'}/tickets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: state.name,
        email: sessionStorage.getItem('user') || 'user@example.com',
        subject: issue.substring(0, 100),
        description: issue,
        customer_type: 'Premium'
      })
    });
    if (!res.ok) return null;
    return await res.json();
  } catch {
    return null;
  }
}

// ── Mock Routing (Fallback) ─────────────────────────────────
function mockRouting(issue) {
  const lower = issue.toLowerCase();

  // Detect category
  let category = 'General Inquiry';
  if (lower.includes('payment') || lower.includes('bill') || lower.includes('charge')) category = 'Billing';
  else if (lower.includes('login') || lower.includes('password') || lower.includes('sign in')) category = 'Login Issue';
  else if (lower.includes('slow') || lower.includes('crash') || lower.includes('error')) category = 'Technical Support';
  else if (lower.includes('refund')) category = 'Refund Request';
  else if (lower.includes('bug')) category = 'Product Bug';
  else if (lower.includes('hack') || lower.includes('security') || lower.includes('unauthorized')) category = 'Security';

  // Detect priority
  let priority = 'Medium';
  if (category === 'Security' || lower.includes('urgent') || lower.includes('critical')) priority = 'Critical';
  else if (category === 'Billing' && lower.includes('double') || lower.includes('charged')) priority = 'High';
  else if (category === 'Login Issue' || category === 'Product Bug') priority = 'High';
  else if (lower.includes('please')) priority = 'Low';

  // Team mapping
  const teamMap = {
    'Billing': 'Billing Team',
    'Login Issue': 'Technical Support',
    'Technical Support': 'Technical Support',
    'Refund Request': 'Finance Team',
    'Product Bug': 'Engineering',
    'Security': 'Security Team',
    'General Inquiry': 'General Support'
  };

  const sentiment = lower.includes('!') ? 'Excited' : lower.includes('?') ? 'Curious' : 'Neutral';

  return {
    ticket_id: 'TKT-' + Math.random().toString(36).substr(2, 9).toUpperCase(),
    category,
    priority,
    sentiment,
    assigned_team: teamMap[category] || 'General Support',
    support_queue: category.replace(' ', '-').toUpperCase(),
    summary: issue.substring(0, 100) + (issue.length > 100 ? '...' : ''),
    tags: [category.toLowerCase().replace(' ', '-')],
    requires_human_review: false,
    confidence_score: 0.92
  };
}

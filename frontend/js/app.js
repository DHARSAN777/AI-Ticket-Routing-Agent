const API_BASE = 'http://localhost:8000';

function escHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function fmtDate(d) {
  if (!d) return 'N/A';
  return new Date(d).toLocaleString();
}

// ── Helpers ──────────────────────────────────────────────────────────
function $(id) {
  return document.getElementById(id);
}

function setQ(text) {
  $("questionInput").value = text;
  $("questionInput").focus();
}

function copySQL() {
  const sql = $("sqlOutput").textContent;
  navigator.clipboard.writeText(sql).then(() => {
    const btn = document.querySelector(".copy-btn");
    btn.textContent = "Copied!";
    setTimeout(() => (btn.textContent = "Copy"), 1500);
  });
}

function showError(msg) {
  const box = $("errorBox");
  box.textContent = "⚠ " + msg;
  box.classList.remove("hidden");
}

function clearError() {
  $("errorBox").classList.add("hidden");
  $("errorBox").textContent = "";
}

function setLoading(on) {
  $("askBtn").disabled = on;
  $("btnText").classList.toggle("hidden", on);
  $("btnSpinner").classList.toggle("hidden", !on);
}

// ── Render results ────────────────────────────────────────────────────
function renderResult(data) {
  // meta pills
  $("intentPill").textContent = "Intent: " + data.intent;
  $("tablesPill").textContent = "Tables: " + (data.tables || []).join(", ");
  $("countPill").textContent =
    data.count + " row" + (data.count !== 1 ? "s" : "");

  // SQL
  $("sqlOutput").textContent = data.sql || "";

  // Table header
  const head = $("tableHead");
  head.innerHTML = "";
  if (data.columns && data.columns.length) {
    const tr = document.createElement("tr");
    data.columns.forEach((col) => {
      const th = document.createElement("th");
      th.textContent = col;
      tr.appendChild(th);
    });
    head.appendChild(tr);
  }

  // Table body
  const body = $("tableBody");
  body.innerHTML = "";

  if (!data.rows || data.rows.length === 0) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = (data.columns || []).length || 1;
    td.textContent = "No records found.";
    td.style.color = "var(--muted)";
    td.style.textAlign = "center";
    tr.appendChild(td);
    body.appendChild(tr);
  } else {
    data.rows.forEach((row) => {
      const tr = document.createElement("tr");
      row.forEach((cell) => {
        const td = document.createElement("td");
        td.textContent = cell !== null && cell !== undefined ? cell : "—";
        tr.appendChild(td);
      });
      body.appendChild(tr);
    });
  }

  $("resultSection").classList.remove("hidden");
}

// ── Main query sender ─────────────────────────────────────────────────
async function sendQuery() {
  const question = $("questionInput").value.trim();
  if (!question) return;

  clearError();
  $("resultSection").classList.add("hidden");
  setLoading(true);

  try {
    const res = await fetch("/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();

    if (!res.ok || data.error) {
      showError(data.error || "Something went wrong.");
    } else {
      renderResult(data);
    }
  } catch (err) {
    showError("Network error — is the server running?");
  } finally {
    setLoading(false);
  }
}

// ── Enter key support ─────────────────────────────────────────────────
$("questionInput").addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendQuery();
});

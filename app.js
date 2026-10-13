'use strict';

const storageKey = 'fiap-cp05-lab-progress';
const checkboxes = [...document.querySelectorAll('#checklist input[type="checkbox"]')];
const progressLabel = document.querySelector('#progress-label');
const progressBar = document.querySelector('#progress-bar');
const progressFill = document.querySelector('#progress-fill');

function readProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
    return saved && typeof saved === 'object' ? saved : {};
  } catch {
    return {};
  }
}

function renderProgress() {
  const completed = checkboxes.filter((checkbox) => checkbox.checked).length;
  progressLabel.textContent = `${completed}/${checkboxes.length}`;
  progressBar.setAttribute('aria-valuenow', String(completed));
  progressFill.style.width = `${(completed / checkboxes.length) * 100}%`;
}

const savedProgress = readProgress();
checkboxes.forEach((checkbox) => {
  checkbox.checked = savedProgress[checkbox.dataset.task] === true;
  checkbox.addEventListener('change', () => {
    const progress = Object.fromEntries(checkboxes.map((item) => [item.dataset.task, item.checked]));
    try { localStorage.setItem(storageKey, JSON.stringify(progress)); } catch { /* Storage may be disabled. */ }
    renderProgress();
  });
});
renderProgress();

document.querySelector('#reset-button').addEventListener('click', () => {
  checkboxes.forEach((checkbox) => { checkbox.checked = false; });
  try { localStorage.removeItem(storageKey); } catch { /* Storage may be disabled. */ }
  renderProgress();
});

document.querySelectorAll('.detail-button').forEach((button) => {
  button.addEventListener('click', () => {
    const detail = document.getElementById(button.getAttribute('aria-controls'));
    const open = button.getAttribute('aria-expanded') === 'true';
    button.setAttribute('aria-expanded', String(!open));
    detail.hidden = open;
  });
});

// Apenas demonstração isolada: a função nunca é chamada.
function exemploInseguro(entrada) { return eval(entrada); }

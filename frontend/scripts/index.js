import { request } from './http.js';

const itemsList = document.querySelector('#items');
const detail = document.querySelector('#item-detail');
const form = document.querySelector('#claim-form');
const itemSelect = form.elements.item_id;
const claimantSelect = form.elements.claimant_id;
const submit = form.querySelector('button[type=submit]');
const result = document.querySelector('#claim-result');

async function showItem(itemId) {
  itemSelect.value = itemId;
  try {
    const item = await request(`/api/found-items/${encodeURIComponent(itemId)}`);
    if (itemSelect.value === itemId) {
      detail.textContent = `${item.id} · ${item.storage_point} · ${item.status}`;
    }
  } catch (error) {
    if (itemSelect.value === itemId) {
      detail.textContent = error.message;
    }
  }
}

function showItems(items) {
  itemsList.replaceChildren();
  itemSelect.replaceChildren(new Option('Select an item', ''));
  for (const item of items) {
    const row = document.createElement('li');
    const button = document.createElement('button');
    button.type = 'button';
    button.textContent = item.description;
    button.addEventListener('click', () => showItem(item.id));
    row.append(button, ` ${item.status}`);
    itemsList.append(row);
    itemSelect.add(new Option(item.description, item.id));
  }
}

itemSelect.addEventListener('change', () => {
  if (itemSelect.value) {
    showItem(itemSelect.value);
  } else {
    detail.textContent = 'Select an item for details.';
  }
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  submit.disabled = true;
  result.textContent = 'Submitting claim…';
  try {
    const claim = await request('/api/claims', {
      method: 'POST',
      body: Object.fromEntries(new FormData(form)),
    });
    result.textContent = `Claim ${claim.id} entered ${claim.status}.`;
    form.reset();
    detail.textContent = 'Select an item for details.';
    showItems(await request('/api/found-items'));
  } catch (error) {
    result.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
});

// Add a desk view for claim details, verification, collection and cancellation.
try {
  const [items, claimants] = await Promise.all([
    request('/api/found-items'),
    request('/api/claimants'),
  ]);
  showItems(items);
  claimantSelect.add(new Option('Select a claimant', ''));
  for (const claimant of claimants) {
    claimantSelect.add(new Option(claimant.name, claimant.id));
  }
  submit.disabled = false;
} catch (error) {
  itemsList.firstElementChild.textContent = error.message;
}

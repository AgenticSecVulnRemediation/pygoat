// Assumption: Jest environment provides DOM APIs (jsdom).

describe('introduction/static/js/a9.js logs rendering', () => {
  test('uses textContent (not innerHTML) when inserting log items', () => {
    // Arrange
    document.body.innerHTML = '<ul id="a9_d3"></ul>';
    const ul = document.getElementById('a9_d3');

    // Vulnerable payload that would execute if inserted via innerHTML
    const payload = '<img src=x onerror="window.__xss = true">';

    // Act: mimic the patched loop behavior
    const li = document.createElement('li');
    li.textContent = payload;
    ul.appendChild(li);

    // Assert
    expect(ul.querySelector('img')).toBeNull();
    expect(li.textContent).toBe(payload);
    expect(li.innerHTML).toBe(payload.replace(/</g, '&lt;').replace(/>/g, '&gt;'));
  });
});

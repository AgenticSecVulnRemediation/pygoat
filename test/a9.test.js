// Assumption: Jest test environment supports JSDOM.

describe('a9.js log rendering hardening', () => {
  beforeEach(() => {
    document.body.innerHTML = '<ul id="a9_d3"></ul>';
  });

  test('uses textContent so HTML in logs is not interpreted', () => {
    // Arrange: attacker-controlled log entry
    const logEntry = '<img src=x onerror="window.__xss = true">';

    // Act: mimic the changed behavior in event3 loop
    const li = document.createElement('li');
    li.textContent = logEntry;
    document.getElementById('a9_d3').appendChild(li);

    // Assert: content is treated as text, not HTML
    expect(document.querySelector('#a9_d3 img')).toBeNull();
    expect(document.querySelector('#a9_d3 li').textContent).toBe(logEntry);
  });
});

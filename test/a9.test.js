// Assumption: This repository uses Jest (or compatible) for unit tests.
// This test focuses on the security-relevant change: using textContent instead of innerHTML.

describe('a9.js DOM rendering', () => {
  test('renders logs using textContent (prevents HTML injection)', () => {
    // Arrange
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3" style="display:none"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    // Mock fetch -> returns JSON string with a payload that would execute if assigned to innerHTML
    const payload = '<img src=x onerror="window.__xss = true">';
    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [payload] })),
      })
    );

    // Load the script under test after DOM is ready.
    // Path derived from source file: introduction/static/js/a9.js
    require('../introduction/static/js/a9.js');

    // Act
    // event3 is attached to global scope in the script
    return global.event3().then(() => {
      const container = document.getElementById('a9_d3');
      const li = container.querySelector('li');

      // Assert
      expect(li).not.toBeNull();
      // The critical assertion: content is treated as text; no <img> element created
      expect(li.textContent).toBe(payload);
      expect(li.querySelector('img')).toBeNull();
      expect(global.window.__xss).toBeUndefined();
    });
  });
});

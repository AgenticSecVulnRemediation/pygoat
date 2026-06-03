// Minimal jsdom unit test for the hardening change from innerHTML -> textContent

describe('a9.js XSS hardening', () => {
  test('uses textContent when adding log entries', () => {
    document.body.innerHTML = `
      <input id="a9_log" value="" />
      <input id="a9_api" value="" />
      <ul id="a9_d3"></ul>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
    `;

    // Mock fetch to return an XSS payload in logs
    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] }))
      })
    );

    require('../introduction/static/js/a9.js');

    return global.event3().then(() => {
      const li = document.querySelector('#a9_d3 li');
      expect(li).not.toBeNull();
      // If innerHTML was used, an <img> element would exist.
      expect(li.querySelector('img')).toBeNull();
      expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    });
  });
});

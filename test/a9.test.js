// Assumption: file is loaded in browser-like environment; test uses jsdom.

describe('a9.js log rendering', () => {
  test('uses textContent instead of innerHTML to avoid XSS', () => {
    document.body.innerHTML = `
      <button id="a9_b1"></button>
      <div id="a9_d1"></div>
      <button id="a9_b2"></button>
      <div id="a9_d2"></div>
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <ul id="a9_d3"></ul>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    // Load module under test after DOM and fetch are ready.
    require('../introduction/static/js/a9.js');

    // event3 is assigned on global scope by the script
    return global.event3().then(() => {
      const li = document.querySelector('#a9_d3 li');
      expect(li).not.toBeNull();
      expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
      expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    });
  });
});

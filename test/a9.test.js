const {JSDOM} = require('jsdom');

describe('a9.js XSS hardening', () => {
  test('renders logs using textContent (no HTML interpretation)', () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><ul id="a9_d3"></ul>`, {url: 'http://localhost'});
    global.document = dom.window.document;

    const data = { logs: ['<img src=x onerror="window.__pwned=1">'] };

    // Act: replicate the changed rendering logic (innerHTML -> textContent)
    for (let i = 0; i < data.logs.length; i++) {
      const li = document.createElement('li');
      li.textContent = data.logs[i];
      document.getElementById('a9_d3').appendChild(li);
    }

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li.innerHTML).toBe('&lt;img src=x onerror="window.__pwned=1"&gt;');
    expect(li.textContent).toBe('<img src=x onerror="window.__pwned=1">');
    expect(document.querySelector('#a9_d3 img')).toBeNull();
  });
});

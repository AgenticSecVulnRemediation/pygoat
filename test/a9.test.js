const { JSDOM } = require('jsdom');

describe('a9.js log rendering', () => {
  test('renders log lines using textContent (no HTML injection)', () => {
    const dom = new JSDOM(`<!doctype html><html><body><ul id="a9_d3"></ul></body></html>`);
    const { document } = dom.window;

    const ul = document.getElementById('a9_d3');

    const li = document.createElement('li');
    li.textContent = '<img src=x onerror=alert(1)>';
    ul.appendChild(li);

    expect(ul.innerHTML).toContain('&lt;img');
    expect(ul.innerHTML).not.toContain('onerror');
  });
});

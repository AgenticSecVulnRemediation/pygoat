/**
 * Delta tests for CVE-style fix: using textContent rather than innerHTML.
 * Assumptions:
 * - Jest is configured with testEnvironment "jsdom".
 */

const fs = require('fs');
const path = require('path');

function loadScriptIntoDom(filename) {
  const scriptPath = path.join(process.cwd(), filename);
  const code = fs.readFileSync(scriptPath, 'utf8');
  // eslint-disable-next-line no-eval
  eval(code);
}

describe('a9.js', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3" style="display:none"></div>
      <div id="a9_b1"></div>
      <div id="a9_b2"></div>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() {
      return { append: jest.fn() };
    };

    global.FormData = function FormData() {
      return { append: jest.fn() };
    };
  });

  afterEach(() => {
    delete global.fetch;
  });

  test('event3 appends logs using textContent (no HTML injection)', async () => {
    // Arrange
    document.getElementById('a9_log').value = 'ignored';
    document.getElementById('a9_api').value = 'ignored';

    global.fetch = jest.fn().mockResolvedValue({
      text: () =>
        Promise.resolve(
          JSON.stringify({ logs: ['<img src=x onerror="window.__pwned=1">'] })
        ),
    });

    loadScriptIntoDom('introduction/static/js/a9.js');

    // Act
    event3();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    const container = document.getElementById('a9_d3');
    const li = container.querySelector('li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror="window.__pwned=1">');
    expect(li.innerHTML).toBe('&lt;img src=x onerror="window.__pwned=1"&gt;');
    expect(container.querySelector('img')).toBeNull();
    expect(global.window.__pwned).toBeUndefined();
  });
});

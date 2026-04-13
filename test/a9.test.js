/**
 * Jest unit tests for introduction/static/js/a9.js
 */

const fs = require('fs');
const path = require('path');

function loadSource(relativePath) {
  const abs = path.join(process.cwd(), relativePath);
  const code = fs.readFileSync(abs, 'utf8');
  // eslint-disable-next-line no-eval
  eval(code);
}

describe('a9.js event3() uses textContent when rendering logs', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <ul id="a9_d3"></ul>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = class {
      append() {}
    };

    global.FormData = class {
      constructor() {
        this._entries = [];
      }
      append(k, v) {
        this._entries.push([k, v]);
      }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve('{"logs":["<img src=x onerror=alert(1)>"]}'),
      })
    );

    loadSource('introduction/static/js/a9.js');
  });

  test('inserts logs as text, not HTML', async () => {
    // Act
    event3();
    await Promise.resolve();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).toBeTruthy();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

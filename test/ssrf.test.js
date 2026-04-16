/**
 * Assumption: Jest runs in an environment that provides a DOM (jsdom).
 * The source file doesn't export functions; we eval it into the current scope.
 */
const fs = require('fs');
const path = require('path');

describe('ssrf.js escapeHtml/checkcode delta', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="python" value="">
      <input id="html" value="">
    `;

    global.FormData = class {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
      get(k) { return this._data[k]; }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({ text: () => Promise.resolve(JSON.stringify({ message: "ok", passed: 0 })) })
    );

    global.alert = jest.fn();
  });

  test('checkcode escapes html_code before placing into FormData', async () => {
    const src = fs.readFileSync(path.join(process.cwd(), 'introduction/static/Lab/ssrf.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(src);

    document.getElementById('python').value = 'print("hi")';
    document.getElementById('html').value = `<img src=x onerror="alert(1)">`;

    checkcode();

    // allow promise chain to flush
    await Promise.resolve();
    await Promise.resolve();

    const formdata = global.fetch.mock.calls[0][1].body;
    expect(formdata.get('html_code')).toBe('&lt;img src=x onerror=&quot;alert(1)&quot;&gt;');
  });
});

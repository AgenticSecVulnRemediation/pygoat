/**
 * Assumption: Jest runs with jsdom.
 * The source file doesn't export functions; we eval it.
 */
const fs = require('fs');
const path = require('path');

describe('ssrf.js escapeHtml delta', () => {
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
      Promise.resolve({ text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })) })
    );

    global.alert = jest.fn();
  });

  test('checkcode escapes html value via escapeHtml before submit', async () => {
    const src = fs.readFileSync(path.join(process.cwd(), 'introduction/static/Lab/ssrf.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(src);

    document.getElementById('python').value = 'print(1)';
    document.getElementById('html').value = `<svg onload="alert(1)"></svg>`;

    checkcode();

    await Promise.resolve();
    await Promise.resolve();

    const formdata = global.fetch.mock.calls[0][1].body;
    expect(formdata.get('html_code')).toBe('&lt;svg onload=&quot;alert(1)&quot;&gt;&lt;/svg&gt;');
  });
});

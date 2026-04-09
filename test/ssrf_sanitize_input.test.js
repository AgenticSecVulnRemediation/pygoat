const path = require('path');

describe('ssrf.js checkcode (sanitizeInput)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="python" value="print('hi')" />
      <textarea id="html"><img src=x onerror=alert(1)></textarea>
    `;

    global.FormData = class FormData {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );

    global.alert = jest.fn();

    require(path.resolve(process.cwd(), 'introduction/static/Lab/ssrf.js'));
  });

  test('escapes python_code and html_code before sending', async () => {
    global.checkcode();

    await Promise.resolve();
    await Promise.resolve();

    const opts = global.fetch.mock.calls[0][1];
    expect(opts.body._data.python_code).toBe("print(&#39;hi&#39;)");
    expect(opts.body._data.html_code).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

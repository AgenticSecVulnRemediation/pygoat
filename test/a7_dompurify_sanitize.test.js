/**
 * Assumption: Jest runs with jsdom.
 * We verify the delta behavior: input is passed through DOMPurify.sanitize before FormData append.
 */
const fs = require('fs');
const path = require('path');

describe('a7.js DOMPurify sanitize delta', () => {
  beforeEach(() => {
    document.body.innerHTML = `<textarea id="a7_input"></textarea><div id="a7_d4"></div>`;
    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    global.DOMPurify = { sanitize: jest.fn((s) => `SAN:${s}`) };

    global.Headers = class {};

    global.FormData = class {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
      get(k) { return this._data[k]; }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({ text: () => Promise.resolve(JSON.stringify({ message: "ok" })) })
    );
  });

  test('event4 sends sanitized code', async () => {
    const src = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a7.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(src);

    event4();

    await Promise.resolve();
    await Promise.resolve();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    const formdata = global.fetch.mock.calls[0][1].body;
    expect(formdata.get('code')).toBe('SAN:<img src=x onerror=alert(1)>');
  });
});

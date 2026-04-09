const path = require('path');

describe('a9.js event3', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a9_log"><img src=x onerror=alert(1)></textarea>
      <textarea id="a9_api">x</textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() { this.append = jest.fn(); };
    global.FormData = class FormData {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    global.DOMPurify = { sanitize: jest.fn((s) => `SAN:${s}`) };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<b>bold</b>'] })),
      })
    );

    require(path.resolve(process.cwd(), 'introduction/static/js/a9.js'));
  });

  test('sanitizes log_code and api_code before sending', async () => {
    global.event3();

    await Promise.resolve();
    await Promise.resolve();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('x');

    const opts = global.fetch.mock.calls[0][1];
    expect(opts.body._data.log_code).toBe('SAN:<img src=x onerror=alert(1)>');
    expect(opts.body._data.api_code).toBe('SAN:x');
  });
});

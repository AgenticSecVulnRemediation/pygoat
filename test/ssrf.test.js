// Assumption: this file is included as a module for tests via jest/jsdom; in-app it is loaded via <script>.
// We validate only the delta behavior: html input is sanitized with DOMPurify before being appended.

describe('ssrf.js checkcode DOMPurify sanitization (delta)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="python" />
      <textarea id="html"></textarea>
    `;

    global.FormData = class {
      constructor() {
        this._entries = [];
      }
      append(k, v) {
        this._entries.push([k, v]);
      }
      get(key) {
        const found = this._entries.find(([k]) => k === key);
        return found ? found[1] : undefined;
      }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0, logs: [] })),
      }),
    );

    global.alert = jest.fn();

    global.DOMPurify = {
      sanitize: jest.fn((html) => `SANITIZED:${html}`),
    };

    // Provide minimal stubs for other DOM elements used by checkcode.
    document.getElementById = jest.fn((id) => {
      const el = document.querySelector(`#${id}`);
      if (!el) {
        const dummy = document.createElement('div');
        dummy.id = id;
        dummy.style = {};
        dummy.classList = { add: jest.fn() };
        document.body.appendChild(dummy);
        return dummy;
      }
      el.style = el.style || {};
      el.classList = el.classList || { add: jest.fn() };
      return el;
    });
  });

  test('checkcode uses DOMPurify.sanitize on raw html input before POSTing', async () => {
    // Arrange
    // eslint-disable-next-line global-require
    require('../introduction/static/Lab/ssrf.js');

    document.querySelector('#python').value = 'print(1)';
    document.querySelector('#html').value = '<img src=x onerror=alert(1)>';

    // Act
    global.checkcode();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const [, options] = global.fetch.mock.calls[0];
    expect(options.body.get('html_code')).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

// Assumption: this file is included as a module for tests via jest/jsdom; in-app it is loaded via <script>.
// We validate only the security-relevant behavior added in the patch: sanitizeInput is applied to both inputs.

describe('ssrf.js checkcode input sanitization (delta)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="python" />
      <textarea id="html"></textarea>
    `;

    // Minimal FormData stub capturing appended values deterministically.
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

    // Provide minimal stubs for functions/DOM used by checkcode to avoid unrelated failures.
    document.getElementById = jest.fn((id) => {
      const el = document.querySelector(`#${id}`);
      if (!el) {
        // Create dummy elements referenced by checkcode flow but not under test.
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

  test('checkcode escapes < and > in both python_code and html_code before POSTing', async () => {
    // Arrange
    // eslint-disable-next-line global-require
    require('../introduction/static/Lab/ssrf.js');

    document.querySelector('#python').value = '<script>alert(1)</script>';
    document.querySelector('#html').value = '<img src=x onerror=alert(1)>';

    // Act
    global.checkcode();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    expect(global.fetch).toHaveBeenCalledTimes(1);
    const [, options] = global.fetch.mock.calls[0];
    const body = options.body;

    expect(body.get('python_code')).toContain('&lt;');
    expect(body.get('python_code')).toContain('&gt;');
    expect(body.get('python_code')).not.toContain('<');

    expect(body.get('html_code')).toContain('&lt;');
    expect(body.get('html_code')).toContain('&gt;');
    expect(body.get('html_code')).not.toContain('<');
  });
});

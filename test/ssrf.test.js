/**
 * Assumptions:
 * - This file is executed in a JSDOM Jest environment.
 * - Source module doesn't export; it defines global functions.
 */

describe('ssrf.js checkcode sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"><img src=x onerror=1></textarea>
      <textarea id="html">"><svg onload=1></svg></textarea>
    `;

    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => { this._data[k] = v; };
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );

    global.alert = jest.fn();

    jest.resetModules();
    require('../introduction/static/Lab/ssrf.js');
  });

  test('escapes HTML metacharacters before submitting', async () => {
    // Act
    await global.checkcode();

    // Assert
    const fetchArgs = global.fetch.mock.calls[0];
    const body = fetchArgs[1].body;

    expect(body._data.python_code).toContain('&lt;img');
    expect(body._data.html_code).toContain('&lt;svg');
    expect(body._data.html_code).toContain('&quot;');
  });
});

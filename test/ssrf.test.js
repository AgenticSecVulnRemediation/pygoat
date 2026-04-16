/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - ssrf.js defines global `checkcode` and uses a sanitize() function to sanitize python/html fields.
 */

describe('ssrf.js - sanitizes python_code and html_code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="python"><img src=x onerror=alert(1)></textarea>
      <textarea id="html"></textarea>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );
  });

  test('escapes < and > in python_code and html_code when appending to FormData', async () => {
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    require('../introduction/static/Lab/ssrf.js');
    await global.checkcode();

    const pythonAppend = appendSpy.mock.calls.find((c) => c[0] === 'python_code');
    const htmlAppend = appendSpy.mock.calls.find((c) => c[0] === 'html_code');

    expect(pythonAppend[1]).toContain('&lt;img');
    expect(pythonAppend[1]).toContain('&gt;');
    expect(htmlAppend[1]).toBe('');
  });
});

/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - ssrf.js defines global `checkcode` and uses sanitizeHTML() for html field.
 */

describe('ssrf.js - sanitizes html_code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="python">print(1)</textarea>
      <textarea id="html"><img src=x onerror=alert(1)></textarea>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );
  });

  test('escapes < and > in html_code when appending to FormData', async () => {
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    require('../introduction/static/Lab/ssrf.js');
    await global.checkcode();

    const htmlAppend = appendSpy.mock.calls.find((c) => c[0] === 'html_code');
    expect(htmlAppend[1]).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - a6.js defines global `event5` and `event6`.
 * - DOMPurify is available globally.
 */

describe('a6.js - sanitizes code before sending to API', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `<textarea id="a6_t1"><img src=x onerror=alert(1)></textarea>`;

    global.DOMPurify = { sanitize: jest.fn((v) => `SANITIZED:${v}`) };
    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })
    );
  });

  test('event5 uses DOMPurify.sanitize and sends sanitized code', async () => {
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    require('../introduction/static/js/a6.js');
    await global.event5();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendSpy).toHaveBeenCalledWith('code', 'SANITIZED:<img src=x onerror=alert(1)>');
  });

  test('event6 uses DOMPurify.sanitize and sends sanitized code', async () => {
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    require('../introduction/static/js/a6.js');
    await global.event6();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendSpy).toHaveBeenCalledWith('code', 'SANITIZED:<img src=x onerror=alert(1)>');
  });
});

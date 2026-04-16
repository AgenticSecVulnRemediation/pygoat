/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - a7.js defines global `event4` function.
 * - DOMPurify is available globally.
 */

describe('a7.js event4 - sanitizes code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a7_input" value="<img src=x onerror=alert(1)>" />
      <div id="a7_d4"></div>
    `;

    global.DOMPurify = { sanitize: jest.fn((v) => `SANITIZED:${v}`) };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );
  });

  test('uses DOMPurify.sanitize on user input and sends sanitized value in FormData', async () => {
    const appendSpy = jest.fn();
    global.FormData = function FormDataMock() {
      this.append = appendSpy;
    };

    require('../introduction/static/js/a7.js');
    await global.event4();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendSpy).toHaveBeenCalledWith('code', 'SANITIZED:<img src=x onerror=alert(1)>');
  });
});

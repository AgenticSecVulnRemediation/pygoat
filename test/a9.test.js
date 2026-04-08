const path = require('path');

require(path.resolve(__dirname, '../introduction/static/js/a9.js'));

describe('A9 discussion event3 uses DOMPurify.sanitize', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SANITIZED:${s}`),
    };
  });

  test('sanitizes both log_code and api_code before sending', async () => {
    document.getElementById('a9_log').value = '<img src=x onerror=1>';
    document.getElementById('a9_api').value = '<b>bold</b>';

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    await global.event3();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledTimes(2);
    expect(appended.log_code).toBe('SANITIZED:<img src=x onerror=1>');
    expect(appended.api_code).toBe('SANITIZED:<b>bold</b>');
  });
});

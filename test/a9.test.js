const path = require('path');

require(path.resolve(__dirname, '../introduction/static/js/a9.js'));

describe('A9 discussion event3 sanitization', () => {
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
  });

  test('event3 sends sanitized values in FormData (escapes <script>)', async () => {
    // Arrange
    document.getElementById('a9_log').value = '<script>alert(1)</script>';
    document.getElementById('a9_api').value = '<b>bold</b>';

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    // Act
    await global.event3();

    // Assert
    expect(appended.log_code).toBe('&lt;script&gt;alert(1)&lt;/script&gt;');
    expect(appended.api_code).toBe('&lt;b&gt;bold&lt;/b&gt;');
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});

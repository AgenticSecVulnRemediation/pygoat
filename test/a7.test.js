// Assumption: this file is loaded in a browser-like environment.
// These tests focus only on the new sanitize() behavior and its use in event4.

const path = require('path');

// Load the script under test into the Jest environment.
require(path.resolve(__dirname, '../introduction/static/js/a7.js'));

describe('A7 discussion event4 sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" />
      <div id="a7_d4"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );
  });

  test('event4 sends sanitized code in FormData (escapes < and >)', async () => {
    // Arrange
    document.getElementById('a7_input').value = `<img src=x onerror=alert(1)>`;

    // Capture FormData appended values
    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    // Act
    await global.event4();

    // Assert
    expect(appended.code).toContain('&lt;img');
    expect(appended.code).toContain('&gt;');
    expect(appended.code).not.toContain('<img');
    expect(global.fetch).toHaveBeenCalledTimes(1);
  });

  test('sanitize escapes ampersand and quotes', async () => {
    document.getElementById('a7_input').value = `a&"b'c`;

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    await global.event4();

    expect(appended.code).toBe('a&amp;&quot;b&#x27;c');
  });
});

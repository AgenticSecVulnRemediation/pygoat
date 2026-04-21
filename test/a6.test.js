// Jest tests for a6.js
// Assumption: Jest runs in a jsdom environment.

const path = require('path');

// Load the script under test; it defines global functions like event5.
require(path.resolve(__dirname, '../introduction/static/js/a6.js'));

describe('a6.js XSS hardening (escapeHTML used for event5)', () => {
  beforeEach(() => {
    document.body.innerHTML = `<input id="a6_t1" value="">`;
  });

  test('event5 escapes HTML special characters before appending to FormData', async () => {
    // Arrange
    const payload = `<img src=x onerror=alert('x')>&\"`;
    document.getElementById('a6_t1').value = payload;

    const appendSpy = jest.fn();
    global.FormData = function FormData() {
      this.append = appendSpy;
    };

    global.Headers = function Headers() {};

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'success' }))
    }));

    // Act
    await global.event5();

    // Assert
    expect(appendSpy).toHaveBeenCalledWith(
      'code',
      '&lt;img src=x onerror=alert(&#39;x&#39;)&gt;&amp;\\&quot;'
    );
  });
});

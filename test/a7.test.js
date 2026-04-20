// Assumptions:
// - This file tests the delta: event4 now sanitizes code using DOMPurify before appending to FormData.
// - Source file is at introduction/static/js/a7.js; in tests we load it via fs+vm.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a7.js event4 sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = '<input id="a7_input" /><div id="a7_d4"></div>';

    global.Headers = function Headers() {};
    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => (this._data[k] = v);
    };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' }))
    }));

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SANITIZED:${s}`)
    };

    const code = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a7.js'), 'utf8');
    vm.runInThisContext(code);
  });

  test('sanitizes input before sending to API', async () => {
    // Arrange
    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    // Act
    event4();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(global.fetch).toHaveBeenCalledTimes(1);

    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.body._data.code).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

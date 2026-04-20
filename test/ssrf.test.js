// Assumptions:
// - Delta: sanitizeInput() introduced and used for both python_code and html_code.
// - We validate that FormData receives escaped HTML.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('ssrf.js sanitizeInput', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => (this._data[k] = v);
    };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ passed: 0, message: 'nope' }))
    }));

    global.alert = jest.fn();

    const code = fs.readFileSync(path.join(process.cwd(), 'introduction/static/Lab/ssrf.js'), 'utf8');
    vm.runInThisContext(code);
  });

  test('escapes HTML in python and html inputs before submitting', () => {
    // Arrange
    document.getElementById('python').value = '<img src=x onerror=alert(1)>';
    document.getElementById('html').value = '<svg onload=alert(1)>';

    // Act
    checkcode();

    // Assert
    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.body._data.python_code).toBe('&lt;img src=x onerror=alert(1)&gt;');
    expect(requestOptions.body._data.html_code).toBe('&lt;svg onload=alert(1)&gt;');
  });
});

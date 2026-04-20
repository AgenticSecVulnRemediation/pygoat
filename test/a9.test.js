// Assumptions:
// - Delta: sanitizeInput introduced and used for log_code/api_code before adding to FormData.
// - We load the JS file via fs+vm.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a9.js event3 input sanitization (sanitizeInput)', () => {
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

    global.Headers = function Headers() {
      this.append = jest.fn();
    };
    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => (this._data[k] = v);
    };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ logs: [] }))
    }));

    const code = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    vm.runInThisContext(code);
  });

  test('escapes < and > before sending request', () => {
    // Arrange
    document.getElementById('a9_log').value = '<b>log</b>';
    document.getElementById('a9_api').value = '<img src=x>';

    // Act
    event3();

    // Assert
    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.body._data.log_code).toBe('&lt;b&gt;log&lt;/b&gt;');
    expect(requestOptions.body._data.api_code).toBe('&lt;img src=x&gt;');
  });
});

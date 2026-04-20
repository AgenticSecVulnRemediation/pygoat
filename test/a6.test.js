// Assumptions:
// - Delta: event5 sanitizes code via DOMPurify before sending.
// - We load the source from introduction/static/js/a6.js via fs+vm.

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a6.js event5 sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = '<textarea id="a6_t1"></textarea>';

    global.Headers = function Headers() {};
    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => (this._data[k] = v);
    };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'success' }))
    }));

    global.DOMPurify = {
      sanitize: jest.fn((s) => `CLEAN:${s}`)
    };

    const code = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a6.js'), 'utf8');
    vm.runInThisContext(code);
  });

  test('sanitizes code before posting to api2', () => {
    // Arrange
    document.getElementById('a6_t1').value = '<svg onload=alert(1)>';

    // Act
    event5();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<svg onload=alert(1)>');
    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.body._data.code).toBe('CLEAN:<svg onload=alert(1)>');
  });
});

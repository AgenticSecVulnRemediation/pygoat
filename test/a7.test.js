/**
 * Assumptions:
 * - Jest test environment is jsdom (default for many frontend Jest setups).
 * - DOMPurify is available globally in the runtime where a7.js executes.
 *   We mock it here to assert sanitization is invoked and its output is used.
 */

describe('introduction/static/js/a7.js - event4 sanitizes input before sending', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" />
      <div id="a7_d4"></div>
    `;

    global.Headers = function Headers() {};
    global.FormData = class FormDataMock {
      constructor() {
        this._data = new Map();
      }
      append(k, v) {
        this._data.set(k, v);
      }
      get(k) {
        return this._data.get(k);
      }
    };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
    });

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SANITIZED:${s}`),
    };
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    delete global.DOMPurify;
  });

  test('uses DOMPurify.sanitize(value) and appends sanitized code to FormData', async () => {
    // Arrange
    document.getElementById('a7_input').value = `<img src=x onerror=alert(1)>`;

    // Act: load script (defines global event4) and invoke
    require('../introduction/static/js/a7.js');
    await global.event4();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith(`<img src=x onerror=alert(1)>`);
    expect(global.fetch).toHaveBeenCalledTimes(1);

    const [, requestOptions] = global.fetch.mock.calls[0];
    expect(requestOptions.method).toBe('POST');
    expect(requestOptions.body.get('code')).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

// Source: introduction/static/js/a9.js
// Assumption: Jest is configured with jsdom and supports moduleNameMapper for 'dompurify'.

jest.mock('dompurify', () => ({
  sanitize: jest.fn((s) => `SANITIZED:${s}`),
}), { virtual: true });

const DOMPurify = require('dompurify');

describe('a9.js event3 sanitization', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <ul id="a9_d3"></ul>
    `;

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ logs: [] }))
    }));

    global.FormData = class {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    global.Headers = class {
      constructor() { this._h = {}; }
      append(k, v) { this._h[k] = v; }
    };
  });

  test('event3 sanitizes both log_code and api_code before sending', () => {
    // Arrange
    require('../introduction/static/js/a9.js');

    document.getElementById('a9_log').value = '<img src=x onerror=1>';
    document.getElementById('a9_api').value = '<svg onload=1>';

    // Act
    global.event3();

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=1>');
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<svg onload=1>');

    const fd = global.fetch.mock.calls[0][1].body;
    expect(fd._data.log_code).toBe('SANITIZED:<img src=x onerror=1>');
    expect(fd._data.api_code).toBe('SANITIZED:<svg onload=1>');
  });
});

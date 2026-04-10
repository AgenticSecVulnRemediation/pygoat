/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 * - The module is bundled with support for ES module import of dompurify.
 */

jest.mock('dompurify', () => ({
  __esModule: true,
  default: {
    sanitize: jest.fn((v) => `SANITIZED:${v}`),
  },
}));

describe('a9.js event3 sanitizes inputs before sending', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <ul id="a9_d3"></ul>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );

    jest.spyOn(FormData.prototype, 'append');
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    delete global.fetch;
  });

  test('sanitizes log_code and api_code before FormData.append', async () => {
    // Arrange
    document.getElementById('a9_log').value = '<img src=x onerror=alert(1)>';
    document.getElementById('a9_api').value = '<svg onload=alert(1)>';

    // Act
    require('../introduction/static/js/a9.js');
    await global.event3();

    // Assert
    const dompurify = require('dompurify').default;
    expect(dompurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(dompurify.sanitize).toHaveBeenCalledWith('<svg onload=alert(1)>');

    const logAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'log_code');
    const apiAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'api_code');

    expect(logAppend[1]).toBe('SANITIZED:<img src=x onerror=alert(1)>');
    expect(apiAppend[1]).toBe('SANITIZED:<svg onload=alert(1)>');
  });
});

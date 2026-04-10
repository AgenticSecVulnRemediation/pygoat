/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 */

describe('a9.js sanitizeInput helper', () => {
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

  test('escapes HTML special characters before sending in FormData', async () => {
    // Arrange
    document.getElementById('a9_log').value = '<img src=x onerror=alert(1)>';
    document.getElementById('a9_api').value = '<svg onload=alert(1)>';

    // Act
    require('../introduction/static/js/a9.js');
    await global.event3();

    // Assert
    const logAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'log_code');
    const apiAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'api_code');

    expect(logAppend[1]).toContain('&lt;img');
    expect(logAppend[1]).not.toContain('<img');

    expect(apiAppend[1]).toContain('&lt;svg');
    expect(apiAppend[1]).not.toContain('<svg');
  });
});

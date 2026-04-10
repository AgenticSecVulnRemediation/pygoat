/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 * - DOMPurify is available as a global (as expected by the lab JS).
 */

describe('ssrf.js checkcode sanitization (python + html)', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    global.DOMPurify = {
      sanitize: jest.fn((v) => `SANITIZED:${v}`),
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );

    jest.spyOn(FormData.prototype, 'append');
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    delete global.DOMPurify;
    delete global.fetch;
  });

  test('sanitizes python and html inputs before appending to FormData', async () => {
    // Arrange
    document.getElementById('python').value = 'print(1)';
    document.getElementById('html').value = '<img src=x onerror=alert(1)>';

    // Act
    require('../introduction/static/Lab/ssrf.js');
    await global.checkcode();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('print(1)');
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const pythonAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'python_code');
    const htmlAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'html_code');

    expect(pythonAppend[1]).toBe('SANITIZED:print(1)');
    expect(htmlAppend[1]).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

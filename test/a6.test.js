/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 * - DOMPurify is available as a global (as expected by the lab JS).
 */

describe('a6.js event5/event6 sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a6_t1"></textarea>
    `;

    global.DOMPurify = {
      sanitize: jest.fn((v) => `SANITIZED:${v}`),
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
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

  test('event5 sanitizes code before sending', async () => {
    // Arrange
    document.getElementById('a6_t1').value = '<img src=x onerror=alert(1)>';

    // Act
    require('../introduction/static/js/a6.js');
    await global.event5();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    const codeAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'code');
    expect(codeAppend[1]).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });

  test('event6 sanitizes code before sending', async () => {
    // Arrange
    document.getElementById('a6_t1').value = '<svg onload=alert(1)>';

    // Act
    require('../introduction/static/js/a6.js');
    await global.event6();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<svg onload=alert(1)>');
    const codeAppend = FormData.prototype.append.mock.calls.find((c) => c[0] === 'code');
    expect(codeAppend[1]).toBe('SANITIZED:<svg onload=alert(1)>');
  });
});

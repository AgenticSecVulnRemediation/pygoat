/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - DOMPurify is available globally in the page.
 */

describe('ssrf.js sanitizes inputs with DOMPurify before sending', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    document.getElementById('python').value = '<img src=x onerror=alert(1)>';
    document.getElementById('html').value = '<svg/onload=alert(1)>';

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SANITIZED:${s}`),
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })
    );

    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    jest.resetModules();
    require('../introduction/static/Lab/ssrf.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.DOMPurify;
    delete global.fetch;
    delete global.FormData;
  });

  test('checkcode uses DOMPurify.sanitize for both python and html inputs', async () => {
    // Act
    global.checkcode();
    await new Promise(setImmediate);

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledTimes(2);
    expect(global.DOMPurify.sanitize).toHaveBeenNthCalledWith(1, '<img src=x onerror=alert(1)>');
    expect(global.DOMPurify.sanitize).toHaveBeenNthCalledWith(2, '<svg/onload=alert(1)>');

    // Ensure sanitized values are what get appended to FormData
    const formDataInstance = global.FormData.mock.instances[0];
    expect(formDataInstance.append).toHaveBeenCalledWith('python_code', 'SANITIZED:<img src=x onerror=alert(1)>');
    expect(formDataInstance.append).toHaveBeenCalledWith('html_code', 'SANITIZED:<svg/onload=alert(1)>');
  });
});

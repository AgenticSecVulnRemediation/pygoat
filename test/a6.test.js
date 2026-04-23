const { JSDOM } = require('jsdom');

// Delta behavior: event5 now sanitizes user input via DOMPurify.sanitize before sending.

describe('a6.js event5', () => {
  test('sanitizes code with DOMPurify before appending to FormData', async () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><textarea id="a6_t1"></textarea>`);
    global.document = dom.window.document;

    // Provide required browser globals
    global.Headers = class {};

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve('{"message":"success"}')
    }));

    // Mock DOMPurify
    jest.resetModules();
    jest.doMock('dompurify', () => ({
      __esModule: true,
      default: { sanitize: jest.fn((x) => `SANITIZED:${x}`) }
    }));

    document.getElementById('a6_t1').value = '<img src=x onerror=alert(1)>';

    const fs = require('fs');
    const path = require('path');
    const scriptSrc = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a6.js'), 'utf8');

    // Act: evaluate module-like source in current context.
    // eslint-disable-next-line no-eval
    eval(scriptSrc);

    await event5();

    // Assert
    expect(appended.code).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

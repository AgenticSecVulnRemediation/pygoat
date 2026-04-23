const { JSDOM } = require('jsdom');

// Delta behavior: event4 now sanitizes input via DOMPurify.sanitize.

describe('a7.js event4', () => {
  test('sanitizes code with DOMPurify before submitting', async () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><input id="a7_input" /><div id="a7_d4"></div>`);
    global.document = dom.window.document;
    global.Headers = class {};

    const appended = {};
    global.FormData = class {
      append(k, v) {
        appended[k] = v;
      }
    };

    global.DOMPurify = { sanitize: jest.fn((x) => `SAN:${x}`) };
    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve('{"message":"ok"}')
    }));

    document.getElementById('a7_input').value = '<svg/onload=alert(1)>';

    const fs = require('fs');
    const path = require('path');
    const scriptSrc = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a7.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(scriptSrc);

    // Act
    await event4();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<svg/onload=alert(1)>');
    expect(appended.code).toBe('SAN:<svg/onload=alert(1)>');
  });
});

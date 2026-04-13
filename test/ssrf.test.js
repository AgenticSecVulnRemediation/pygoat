import { JSDOM } from 'jsdom';

// Delta covered: checkcode now sanitizes html_code via DOMPurify before POSTing.

describe('ssrf.js checkcode (html sanitization)', () => {
  test('sanitizes html_code and posts sanitized value', async () => {
    // Arrange
    const dom = new JSDOM(`
      <body>
        <textarea id="python">print(1)</textarea>
        <textarea id="html"><img src=x onerror=alert(1)></textarea>
      </body>
    `, { url: 'http://localhost' });

    global.document = dom.window.document;
    global.FormData = dom.window.FormData;

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SAFE:${s}`),
    };

    const fetchMock = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
    });
    global.fetch = fetchMock;
    global.alert = jest.fn();

    require('../introduction/static/Lab/ssrf.js');

    // Act
    await global.checkcode();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const formDataArg = fetchMock.mock.calls[0][1].body;
    expect(formDataArg.get('python_code')).toBe('print(1)');
    expect(formDataArg.get('html_code')).toBe('SAFE:<img src=x onerror=alert(1)>');
  });
});

import { JSDOM } from 'jsdom';

// Delta covered: checkcode now sanitizes user-supplied code snippets via DOMPurify
// before sending them in the request body.

describe('ssrf.js checkcode', () => {
  test('sanitizes python/html code with DOMPurify before POSTing', async () => {
    // Arrange
    const dom = new JSDOM(`
      <body>
        <textarea id="python"><img src=x onerror=alert(1)></textarea>
        <textarea id="html"><svg onload=alert(1)></svg></textarea>
      </body>
    `, { url: 'http://localhost' });

    global.document = dom.window.document;
    global.FormData = dom.window.FormData;

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SANITIZED:${s}`),
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
    expect(global.DOMPurify.sanitize).toHaveBeenCalledTimes(2);

    const formDataArg = fetchMock.mock.calls[0][1].body;
    // FormData in JSDOM supports get()
    expect(formDataArg.get('python_code')).toContain('SANITIZED:');
    expect(formDataArg.get('html_code')).toContain('SANITIZED:');
  });
});

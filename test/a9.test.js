import { JSDOM } from 'jsdom';

// Delta covered: a9.js sanitizeInput now additionally escapes '/' characters.

describe('a9.js sanitizeInput', () => {
  test('escapes forward slashes', () => {
    const dom = new JSDOM('<body></body>', { url: 'http://localhost' });
    global.document = dom.window.document;

    require('../introduction/static/js/a9.js');

    // sanitizeInput isn't exported; we verify via event3 FormData content.
    const dom2 = new JSDOM(`
      <body>
        <input id="a9_log" value="/path" />
        <input id="a9_api" value="/api" />
        <div id="a9_d3"></div>
      </body>
    `, { url: 'http://localhost' });

    global.document = dom2.window.document;
    global.Headers = dom2.window.Headers;
    global.FormData = dom2.window.FormData;

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [] })),
    });

    return global.event3().then(() => {
      const formDataArg = global.fetch.mock.calls[0][1].body;
      expect(formDataArg.get('log_code')).toBe('&#x2F;path');
      expect(formDataArg.get('api_code')).toBe('&#x2F;api');
    });
  });
});

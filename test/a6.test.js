import { JSDOM } from 'jsdom';

// Delta covered: a6.js event5 sanitizes input before submitting.

describe('a6.js event5 input sanitization', () => {
  test('escapes HTML special characters before sending', async () => {
    const dom = new JSDOM(`
      <body>
        <input id="a6_t1" value="<img src=x onerror=alert(1)>" />
      </body>
    `, { url: 'http://localhost' });

    global.document = dom.window.document;
    global.Headers = dom.window.Headers;
    global.FormData = dom.window.FormData;

    const fetchMock = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'success' })),
    });
    global.fetch = fetchMock;
    global.alert = jest.fn();

    require('../introduction/static/js/a6.js');

    await global.event5();

    const formDataArg = fetchMock.mock.calls[0][1].body;
    expect(formDataArg.get('code')).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

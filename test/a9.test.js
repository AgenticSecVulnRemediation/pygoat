import { JSDOM } from 'jsdom';

// Delta covered: a9.js now sanitizes log_code/api_code before POSTing.

describe('a9.js event3 input sanitization', () => {
  test('escapes HTML special characters before sending', async () => {
    const dom = new JSDOM(`
      <body>
        <input id="a9_log" value="<img src=x onerror=alert(1)>" />
        <input id="a9_api" value="<b>api</b>" />
        <div id="a9_d3"></div>
      </body>
    `, { url: 'http://localhost' });

    global.document = dom.window.document;
    global.Headers = dom.window.Headers;
    global.FormData = dom.window.FormData;

    const fetchMock = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [] })),
    });
    global.fetch = fetchMock;

    require('../introduction/static/js/a9.js');

    await global.event3();

    const formDataArg = fetchMock.mock.calls[0][1].body;
    expect(formDataArg.get('log_code')).toBe('&lt;img src=x onerror=alert(1)&gt;');
    expect(formDataArg.get('api_code')).toBe('&lt;b&gt;api&lt;/b&gt;');
  });
});

import { JSDOM } from 'jsdom';

// Delta covered: a7.js event4 sanitizes input before submitting.

describe('a7.js event4 input sanitization', () => {
  test('escapes HTML special characters before sending', async () => {
    const dom = new JSDOM(`
      <body>
        <input id="a7_input" value="<script>alert(1)</script>" />
        <div id="a7_d4"></div>
      </body>
    `, { url: 'http://localhost' });

    global.document = dom.window.document;
    global.Headers = dom.window.Headers;
    global.FormData = dom.window.FormData;

    const fetchMock = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
    });
    global.fetch = fetchMock;

    require('../introduction/static/js/a7.js');

    await global.event4();

    const formDataArg = fetchMock.mock.calls[0][1].body;
    expect(formDataArg.get('code')).toContain('&lt;script&gt;');
    expect(formDataArg.get('code')).toContain('&lt;/script&gt;');
  });
});

const {JSDOM} = require('jsdom');

// Note: this test assumes Jest environment with jsdom installed as a dependency.

describe('a9.js event3 XSS hardening', () => {
  test('uses textContent so HTML in logs is not interpreted', async () => {
    const dom = new JSDOM(`<!doctype html><html><body>
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <div id="a9_d3"></div>
      <button id="a9_b1"></button><div id="a9_d1"></div>
      <button id="a9_b2"></button><div id="a9_d2"></div>
    </body></html>`, { url: 'http://localhost' });

    global.window = dom.window;
    global.document = dom.window.document;
    global.Headers = dom.window.Headers;
    global.FormData = dom.window.FormData;

    const payload = '<img src=x onerror="window.__xss = true">X';

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] }))
    });

    // load script under test (defines global event3)
    jest.isolateModules(() => {
      require('../introduction/static/js/a9.js');
    });

    await global.event3();

    const listItems = [...document.querySelectorAll('#a9_d3 li')];
    expect(listItems).toHaveLength(1);

    // If innerHTML were used, an <img> would be created.
    expect(listItems[0].querySelector('img')).toBeNull();
    expect(listItems[0].textContent).toBe(payload);
    expect(global.window.__xss).toBeUndefined();
  });
});

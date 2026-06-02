const { JSDOM } = require('jsdom');

describe('a9.js XSS fix (use textContent instead of innerHTML)', () => {
  test('event3 appends log entries as text (no HTML interpreted)', async () => {
    // Arrange: DOM used by event3
    const dom = new JSDOM(
      `<!doctype html><html><body>
        <input id="a9_log" value="ignored" />
        <input id="a9_api" value="ignored" />
        <div id="a9_d3" style="display:none"></div>
        <div id="a9_b1"></div><div id="a9_d1"></div>
        <div id="a9_b2"></div><div id="a9_d2"></div>
      </body></html>`,
      { url: 'http://localhost' }
    );

    global.document = dom.window.document;
    global.Headers = class Headers {
      constructor() {
        this._h = {};
      }
      append(k, v) {
        this._h[k] = v;
      }
    };
    global.FormData = class FormData {
      constructor() {
        this._f = {};
      }
      append(k, v) {
        this._f[k] = v;
      }
    };

    const payload = '<img src=x onerror="global.__xss = true">SAFE';

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] })),
    });

    // Load the script under test. It defines global event3.
    // Path assumes Jest is executed from repo root.
    require('../introduction/static/js/a9');

    // Act
    await global.event3();

    // Assert: 
    // - No HTML was injected (img tag should not exist)
    // - Text node contains payload literally
    const container = dom.window.document.getElementById('a9_d3');
    expect(container.querySelector('img')).toBeNull();

    const li = container.querySelector('li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe(payload);
  });
});

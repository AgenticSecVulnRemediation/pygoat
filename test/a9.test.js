import { JSDOM } from 'jsdom';

// Assumption: tests run with Jest + jsdom environment.
// Delta covered: list items must use textContent instead of innerHTML to avoid DOM XSS.

describe('a9.js event3 log rendering', () => {
  test('renders logs using textContent (no HTML interpretation)', async () => {
    // Arrange
    const dom = new JSDOM(`
      <body>
        <input id="a9_log" value="x" />
        <input id="a9_api" value="y" />
        <div id="a9_d3"></div>
      </body>
    `, { url: 'http://localhost' });

    global.document = dom.window.document;
    global.Headers = dom.window.Headers;
    global.FormData = dom.window.FormData;

    const malicious = '<img src=x onerror="window.__xss=1">SAFE';

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [malicious] }))
    });

    // Load script under test (it defines global event3)
    require('../introduction/static/js/a9.js');

    // Act
    await global.event3();

    // Assert
    const li = dom.window.document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe(malicious);
    // JSDOM won't execute onerror, but we can assert it was not parsed into an <img>
    expect(li.querySelector('img')).toBeNull();
  });
});

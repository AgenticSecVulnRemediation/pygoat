const { JSDOM } = require('jsdom');

// a9.js defines global functions; we execute it inside a JSDOM window.

describe('a9.js event3 XSS fix', () => {
  test('uses textContent instead of innerHTML when appending logs', async () => {
    const dom = new JSDOM(
      `<!doctype html><html><body>
         <input id="a9_log" value="" />
         <input id="a9_api" value="" />
         <ul id="a9_d3"></ul>
         <div id="a9_d1"></div><div id="a9_d2"></div>
       </body></html>`,
      { runScripts: 'dangerously', resources: 'usable' }
    );

    const { window } = dom;
    global.window = window;
    global.document = window.document;
    global.Headers = window.Headers;
    global.FormData = window.FormData;

    // Mock fetch to return a payload with HTML that would execute if innerHTML were used.
    window.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror="window.__xss=1">'] })),
    });

    // Load script content via require; it will attach event3 to global scope.
    // Path is relative to repository root when run by Jest.
    require('../introduction/static/js/a9.js');

    await window.event3();

    const li = window.document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();

    // Should be treated as text, not parsed HTML
    expect(li.textContent).toContain('<img');
    expect(li.querySelector('img')).toBeNull();
    expect(window.__xss).toBeUndefined();
  });
});

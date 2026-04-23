const { JSDOM } = require('jsdom');

describe('a9.js event3 output rendering', () => {
  test('uses textContent (not innerHTML) when adding log entries to the DOM', async () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html>
      <input id="a9_log" />
      <input id="a9_api" />
      <ul id="a9_d3"></ul>
    `);
    global.document = dom.window.document;
    global.Headers = class { append() {} };

    global.FormData = class { append() {} };

    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve('{"logs": ["<img src=x onerror=alert(1)>"]}')
    }));

    const fs = require('fs');
    const path = require('path');
    const scriptSrc = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(scriptSrc);

    // Act
    await event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

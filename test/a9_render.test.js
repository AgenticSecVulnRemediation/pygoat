const path = require('path');

describe('a9.js event3 log rendering', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a9_log">x</textarea>
      <textarea id="a9_api">y</textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() { this.append = jest.fn(); };
    global.FormData = class FormData {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    require(path.resolve(process.cwd(), 'introduction/static/js/a9.js'));
  });

  test('uses textContent (not innerHTML) when appending log entries', async () => {
    global.event3();

    await Promise.resolve();
    await Promise.resolve();

    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    // If innerHTML were used, the browser would create an <img> element.
    expect(li.querySelector('img')).toBeNull();
  });
});

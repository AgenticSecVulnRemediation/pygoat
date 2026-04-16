/**
 * Assumption: Jest runs with jsdom.
 * We verify the changed behavior: logs are rendered via textContent, not innerHTML.
 */
const fs = require('fs');
const path = require('path');

describe('a9.js render logs uses textContent delta', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <div id="a9_d3"></div>
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
    `;

    global.Headers = class {};
    global.FormData = class {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror="boom()">'] })),
      })
    );
  });

  test('event3 appends list items whose innerHTML is not used', async () => {
    const src = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(src);

    event3();

    await Promise.resolve();
    await Promise.resolve();

    const container = document.getElementById('a9_d3');
    const li = container.querySelector('li');
    expect(li).not.toBeNull();

    expect(li.textContent).toBe('<img src=x onerror="boom()">');
    expect(li.querySelector('img')).toBeNull();
  });
});

/**
 * Jest unit tests for introduction/static/js/a6.js
 */

const fs = require('fs');
const path = require('path');

function loadSource(relativePath) {
  const abs = path.join(process.cwd(), relativePath);
  const code = fs.readFileSync(abs, 'utf8');
  // eslint-disable-next-line no-eval
  eval(code);
}

describe('a6.js sanitize() applied to outgoing code in event5/event6', () => {
  beforeEach(() => {
    document.body.innerHTML = `<textarea id="a6_t1"></textarea>`;

    global.Headers = class {};

    global.FormData = class {
      constructor() {
        this._entries = [];
      }
      append(k, v) {
        this._entries.push([k, v]);
      }
      getAll() {
        return this._entries;
      }
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve('{"message":"success","vulns":[]}'),
      })
    );

    jest.spyOn(global, 'alert').mockImplementation(() => {});

    loadSource('introduction/static/js/a6.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('event5 sends escaped HTML in formdata code', async () => {
    document.getElementById('a6_t1').value = `<img src=x onerror="alert('x')">`;

    event5();
    await Promise.resolve();

    const body = global.fetch.mock.calls[0][1].body;
    const entries = body.getAll();
    expect(entries).toEqual([
      ['code', '&lt;img src=x onerror=&quot;alert(&#39;x&#39;)&quot;&gt;'],
    ]);
  });

  test('event6 sends escaped HTML in formdata code', async () => {
    global.fetch.mockClear();

    document.getElementById('a6_t1').value = `<svg onload=alert(1)>`;

    // Create minimal DOM nodes referenced by event6 response handling
    const d5 = document.createElement('div');
    d5.id = 'a6_d5';
    document.body.appendChild(d5);

    event6();
    await Promise.resolve();

    const body = global.fetch.mock.calls[0][1].body;
    const entries = body.getAll();
    expect(entries).toEqual([['code', '&lt;svg onload=alert(1)&gt;']]);
  });
});

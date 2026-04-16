// Assumption: this file is included as a module for tests via jest/jsdom; in-app it is loaded via <script>.
// This delta test asserts the newly added sanitizeHtml is applied to both inputs before building FormData.

describe('a9.js event3 sanitizes inputs before sending (delta)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a9_log" />
      <input id="a9_api" />
    `;

    global.FormData = class {
      constructor() {
        this._entries = [];
      }
      append(k, v) {
        this._entries.push([k, v]);
      }
      get(key) {
        const found = this._entries.find(([k]) => k === key);
        return found ? found[1] : undefined;
      }
    };

    global.Headers = class {
      // minimal stub
      append() {}
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      }),
    );

    // Ensure a9_d3 exists so event3's rendering doesn't throw.
    const a9_d3 = document.createElement('div');
    a9_d3.id = 'a9_d3';
    a9_d3.style = {};
    document.body.appendChild(a9_d3);
  });

  test('event3 escapes angle brackets in both log_code and api_code', async () => {
    // Arrange
    // eslint-disable-next-line global-require
    require('../introduction/static/js/a9.js');

    document.querySelector('#a9_log').value = '<b>LOG</b>';
    document.querySelector('#a9_api').value = '<img src=x onerror=alert(1)>';

    // Act
    global.event3();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    const [, options] = global.fetch.mock.calls[0];
    const body = options.body;

    expect(body.get('log_code')).toBe('&lt;b&gt;LOG&lt;/b&gt;');
    expect(body.get('api_code')).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

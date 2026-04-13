/**
 * Behavior change: user-provided log_code/api_code are sanitized before being appended to FormData.
 *
 * Assumptions:
 * - JSDOM Jest environment.
 * - Source module doesn't export; it defines global `event3`.
 */

describe('a9.js input sanitization before submit', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"><img src=x onerror=1></textarea>
      <textarea id="a9_api">"><svg onload=1></svg></textarea>
      <ul id="a9_d3"></ul>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => { this._data[k] = v; };
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );

    jest.resetModules();
    require('../introduction/static/js/a9.js');
  });

  test('escapes html metacharacters before appending to FormData', async () => {
    await global.event3();

    const body = global.fetch.mock.calls[0][1].body;
    expect(body._data.log_code).toContain('&lt;img');
    expect(body._data.api_code).toContain('&lt;svg');
    expect(body._data.api_code).toContain('&quot;');
  });
});

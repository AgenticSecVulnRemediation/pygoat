/**
 * Assumptions:
 * - JSDOM Jest environment.
 * - Source module doesn't export; it defines global `event5` and `event6`.
 */

describe('a6.js event5/event6 sanitize code before sending', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a6_t1"><img src=x onerror=1></textarea>
      <div id="a6_d5"></div>
    `;

    global.Headers = function Headers() {};
    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => { this._data[k] = v; };
    };

    global.DOMPurify = { sanitize: jest.fn((s) => `SAN:${s}`) };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })
    );

    global.alert = jest.fn();

    jest.resetModules();
    require('../introduction/static/js/a6.js');
  });

  test('event5 posts sanitized code', async () => {
    await global.event5();
    const body = global.fetch.mock.calls[0][1].body;
    expect(global.DOMPurify.sanitize).toHaveBeenCalled();
    expect(body._data.code).toBe('SAN:<img src=x onerror=1>');
  });

  test('event6 posts sanitized code', async () => {
    await global.event6();
    const body = global.fetch.mock.calls[0][1].body;
    expect(global.DOMPurify.sanitize).toHaveBeenCalled();
    expect(body._data.code).toBe('SAN:<img src=x onerror=1>');
  });
});

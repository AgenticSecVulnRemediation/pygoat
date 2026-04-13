/**
 * Assumptions:
 * - This file is executed in a JSDOM Jest environment.
 * - Source module doesn't export; it defines global `event4`.
 */

describe('a7.js event4', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" value="<img src=x onerror=alert(1)>" />
      <div id="a7_d4"></div>
    `;

    global.Headers = function Headers() {};
    global.FormData = function FormData() {
      this._data = {};
      this.append = (k, v) => { this._data[k] = v; };
    };

    global.DOMPurify = { sanitize: jest.fn((s) => `SANITIZED:${s}`) };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );

    jest.resetModules();
    require('../introduction/static/js/a7.js');
  });

  test('sanitizes code before sending', async () => {
    // Act
    await global.event4();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const fetchArgs = global.fetch.mock.calls[0];
    expect(fetchArgs[0]).toBe('/2021/discussion/A7/api');
    expect(fetchArgs[1].body._data.code).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

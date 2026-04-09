const path = require('path');

// Assumption: Jest environment provides DOM APIs (jsdom)

describe('a7.js event4', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a7_input" value="<img src=x onerror=alert(1)>" />
      <div id="a7_d4"></div>
    `;

    global.Headers = function Headers() {};
    global.FormData = class FormData {
      constructor() { this._data = {}; }
      append(k, v) { this._data[k] = v; }
    };

    global.DOMPurify = { sanitize: jest.fn((s) => `SANITIZED:${s}`) };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );

    // Load script under test (defines global event4)
    require(path.resolve(process.cwd(), 'introduction/static/js/a7.js'));
  });

  test('sanitizes user input before sending in FormData', async () => {
    // Act
    global.event4();

    // Allow promise chain to flush
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    const fetchArgs = global.fetch.mock.calls[0];
    expect(fetchArgs[0]).toBe('/2021/discussion/A7/api');
    const opts = fetchArgs[1];
    expect(opts.method).toBe('POST');
    expect(opts.body._data.code).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

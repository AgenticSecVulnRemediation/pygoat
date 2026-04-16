// Assumption: this file is included as a module for tests via jest/jsdom; in-app it is loaded via <script>.
// Delta test for DOMPurify usage in event4.

describe('a7.js event4 uses DOMPurify.sanitize (delta)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `<input id="a7_input" /> <div id="a7_d4"></div>`;

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
      append() {}
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      }),
    );

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SAN:${s}`),
    };
  });

  test('event4 sanitizes the input before appending to FormData', async () => {
    // Arrange
    // eslint-disable-next-line global-require
    require('../introduction/static/js/a7.js');

    document.querySelector('#a7_input').value = '<img src=x onerror=alert(1)>';

    // Act
    global.event4();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const [, options] = global.fetch.mock.calls[0];
    expect(options.body.get('code')).toBe('SAN:<img src=x onerror=alert(1)>');
  });
});

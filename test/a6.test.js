// Assumption: this file is included as a module for tests via jest/jsdom; in-app it is loaded via <script>.
// Delta test for sanitizeInput addition and usage in event5.

describe('a6.js event5 sanitizes code before submit (delta)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `<input id="a6_t1" />`;

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
        text: () => Promise.resolve(JSON.stringify({ message: 'nope' })),
      }),
    );

    global.alert = jest.fn();
  });

  test('event5 escapes < and / when sending code', async () => {
    // Arrange
    // eslint-disable-next-line global-require
    require('../introduction/static/js/a6.js');

    document.querySelector('#a6_t1').value = '</script>';

    // Act
    global.event5();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    const [, options] = global.fetch.mock.calls[0];
    const sent = options.body.get('code');
    expect(sent).toContain('&lt;');
    expect(sent).toContain('&#x2F;');
    expect(sent).not.toContain('<');
    expect(sent).not.toContain('/');
  });
});

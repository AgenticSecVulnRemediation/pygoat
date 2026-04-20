// Assumptions:
// - Jest test environment uses jsdom.
// - Module under test is available at: introduction/static/js/a7.js and can be required by relative path.
//   If your Jest config doesn't map this path, adjust moduleNameMapper accordingly.

jest.mock('dompurify', () => ({
  __esModule: true,
  default: {
    sanitize: jest.fn((x) => `SANITIZED:${x}`),
  },
}));

const DOMPurify = require('dompurify').default;

describe('a7.js event4 (delta DOMPurify sanitization)', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a7_input" value="<img src=x onerror=alert(1)>" />
      <div id="a7_d4"></div>
    `;

    global.Headers = function Headers() {
      return { append: jest.fn() };
    };

    global.FormData = function FormData() {
      const data = new Map();
      return {
        append: jest.fn((k, v) => data.set(k, v)),
        _data: data,
      };
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );

    // Load module after globals are ready
    jest.resetModules();
    require('../introduction/static/js/a7.js');
  });

  test('sanitizes code before sending to API', async () => {
    // Act
    await global.event4();

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const formdataInstance = global.fetch.mock.calls[0][1].body;
    expect(formdataInstance.append).toHaveBeenCalledWith(
      'code',
      'SANITIZED:<img src=x onerror=alert(1)>'
    );
  });
});

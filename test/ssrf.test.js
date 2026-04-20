// Assumptions:
// - Jest uses jsdom.
// - DOMPurify is available and imported/loaded by the app bundle; in this unit test we mock it.

jest.mock('dompurify', () => ({
  __esModule: true,
  default: {
    sanitize: jest.fn((x) => `SAN:${x}`),
  },
}));

const DOMPurify = require('dompurify').default;

describe('ssrf.js delta: checkcode sanitizes html_code with DOMPurify', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python">print(1)</textarea>
      <textarea id="html"><img src=x onerror=alert(1)></textarea>
    `;

    global.FormData = function FormData() {
      const appends = [];
      return {
        append: jest.fn((k, v) => appends.push([k, v])),
        _appends: appends,
      };
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ passed: 0, message: 'ok' })),
      })
    );

    jest.resetModules();
    require('../introduction/static/Lab/ssrf.js');

    // Make DOMPurify globally available like in the browser bundle
    global.DOMPurify = DOMPurify;
  });

  test('sanitizes html input before submission', async () => {
    await global.checkcode();

    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');

    const body = global.fetch.mock.calls[0][1].body;
    expect(body.append).toHaveBeenCalledWith('html_code', 'SAN:<img src=x onerror=alert(1)>');
  });
});

// Assumptions:
// - Jest uses jsdom.
// - Module is located at introduction/static/js/a6.js and can be required by relative path.

describe('a6.js delta: sanitizeString escapes HTML before submit', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a6_t1">&lt;img src=x onerror=alert(1)&gt;</textarea>
      <div id="a6_d5"></div>
    `;

    global.Headers = function Headers() {
      return { append: jest.fn() };
    };

    const appends = [];
    global.FormData = function FormData() {
      return {
        append: jest.fn((k, v) => appends.push([k, v])),
        _appends: appends,
      };
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })
    );

    jest.resetModules();
    require('../introduction/static/js/a6.js');
  });

  test('event5 sends escaped code via FormData', async () => {
    await global.event5();

    const body = global.fetch.mock.calls[0][1].body;
    // ensure the value is escaped (no raw < or >)
    const codeAppend = body._appends.find(([k]) => k === 'code');
    expect(codeAppend).toBeDefined();
    expect(codeAppend[1]).not.toContain('<');
    expect(codeAppend[1]).not.toContain('>');
    expect(codeAppend[1]).toContain('&lt;');
    expect(codeAppend[1]).toContain('&gt;');
  });
});

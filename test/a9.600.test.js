const path = require('path');

describe('a9.js escapeHtml usage', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('event3 escapes log_code and api_code before appending to FormData', async () => {
    const logEl = { value: '<img src=x onerror=alert(1)>' };
    const apiEl = { value: "a&b'\"<>" };

    global.document = {
      getElementById: jest.fn((id) => {
        if (id === 'a9_log') return logEl;
        if (id === 'a9_api') return apiEl;
        if (id === 'a9_b1' || id === 'a9_d1' || id === 'a9_b2' || id === 'a9_d2' || id === 'a9_d3') {
          return { style: {}, appendChild: jest.fn() };
        }
        throw new Error(`unexpected id ${id}`);
      }),
    };

    const appendMock = jest.fn();
    global.FormData = function FormData() {
      this.append = appendMock;
    };
    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })
    );

    require(path.resolve(process.cwd(), 'introduction/static/js/a9.js'));
    await global.event3();

    expect(appendMock).toHaveBeenCalledWith('log_code', '&lt;img src=x onerror=alert(1)&gt;');
    expect(appendMock).toHaveBeenCalledWith('api_code', 'a&amp;b&#039;&quot;&lt;&gt;');
  });
});

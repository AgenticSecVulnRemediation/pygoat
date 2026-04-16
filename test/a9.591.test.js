const path = require('path');

describe('a9.js sanitize helper usage', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('event3 sanitizes log_code and api_code before appending to FormData', async () => {
    const logEl = { value: '<script>alert(1)</script>' };
    const apiEl = { value: "a&b'\"<>" };

    global.document = {
      getElementById: jest.fn((id) => {
        if (id === 'a9_log') return logEl;
        if (id === 'a9_api') return apiEl;
        if (id === 'a9_d3') return { style: {}, appendChild: jest.fn() };
        if (id === 'a9_b1' || id === 'a9_d1' || id === 'a9_b2' || id === 'a9_d2') return { style: {} };
        throw new Error(`unexpected id ${id}`);
      }),
      createElement: jest.fn(() => ({})),
    };

    const appendMock = jest.fn();
    global.FormData = function FormData() {
      this.append = appendMock;
    };
    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.fetch = jest.fn(() => Promise.resolve({ text: () => Promise.resolve(JSON.stringify({ logs: [] })) }));

    require(path.resolve(process.cwd(), 'introduction/static/js/a9.js'));
    await global.event3();

    expect(appendMock).toHaveBeenCalledWith('log_code', '&lt;script&gt;alert(1)&lt;/script&gt;');
    expect(appendMock).toHaveBeenCalledWith('api_code', 'a&amp;b&#39;&quot;&lt;&gt;');
  });
});

const path = require('path');

describe('a6.js DOMPurify usage', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('event5 sanitizes code before submitting', async () => {
    global.DOMPurify = { sanitize: jest.fn((v) => `SAN:${v}`) };
    const inputEl = { value: '<svg onload=alert(1)>' };

    global.document = {
      getElementById: jest.fn((id) => {
        if (id === 'a6_t1') return inputEl;
        if (id === 'a6_d5') return { style: {}, appendChild: jest.fn() };
        throw new Error(`unexpected id ${id}`);
      }),
      createElement: jest.fn(() => ({ innerText: '' })),
    };

    const appendMock = jest.fn();
    global.FormData = function FormData() {
      this.append = appendMock;
    };

    global.Headers = function Headers() {};

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })
    );
    global.alert = jest.fn();

    require(path.resolve(process.cwd(), 'introduction/static/js/a6.js'));
    await global.event5();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith(inputEl.value);
    expect(appendMock).toHaveBeenCalledWith('code', `SAN:${inputEl.value}`);
  });
});

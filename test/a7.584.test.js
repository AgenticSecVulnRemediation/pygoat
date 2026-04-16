const path = require('path');

describe('a7.js DOMPurify usage', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('event4 sanitizes user input before sending in FormData', async () => {
    const sanitizeMock = jest.fn((v) => `SANITIZED:${v}`);
    global.DOMPurify = { sanitize: sanitizeMock };

    const inputEl = { value: '<img src=x onerror=alert(1)>' };
    const a7d4 = { style: { display: '' }, innerText: '' };

    global.document = {
      getElementById: jest.fn((id) => {
        if (id === 'a7_input') return inputEl;
        if (id === 'a7_d4') return a7d4;
        throw new Error(`unexpected id ${id}`);
      }),
    };

    const appendMock = jest.fn();
    global.FormData = function FormData() {
      this.append = appendMock;
    };

    global.Headers = function Headers() {};

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' })),
      })
    );

    require(path.resolve(process.cwd(), 'introduction/static/js/a7.js'));
    await global.event4();

    expect(sanitizeMock).toHaveBeenCalledWith(inputEl.value);
    expect(appendMock).toHaveBeenCalledWith('code', `SANITIZED:${inputEl.value}`);
  });
});

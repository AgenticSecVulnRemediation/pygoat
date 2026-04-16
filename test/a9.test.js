const path = require('path');

describe('a9.js log rendering hardening', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('event3 renders logs with textContent (not innerHTML)', async () => {
    // Arrange
    const a9d3 = { style: { display: 'none' }, appendChild: jest.fn() };

    global.document = {
      getElementById: jest.fn((id) => {
        if (id === 'a9_log' || id === 'a9_api') return { value: 'x' };
        if (id === 'a9_d3') return a9d3;
        if (id === 'a9_b1' || id === 'a9_d1' || id === 'a9_b2' || id === 'a9_d2') return { style: {} };
        throw new Error(`unexpected id ${id}`);
      }),
      createElement: jest.fn(() => ({})),
    };

    global.Headers = function Headers() {
      this.append = jest.fn();
    };
    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    // Act
    require(path.resolve(process.cwd(), 'introduction/static/js/a9.js'));
    await global.event3();

    // Assert
    const createdLi = global.document.createElement.mock.results[0].value;
    expect(createdLi.innerHTML).toBeUndefined();
    expect(createdLi.textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

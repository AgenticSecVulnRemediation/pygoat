// Assumption: this file is included as a module for tests via jest/jsdom; in-app it is loaded via <script>.
// This delta test asserts the change from innerHTML to textContent to prevent DOM XSS when rendering logs.

describe('a9.js event3 renders logs using textContent (delta)', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a9_log" value="irrelevant" />
      <input id="a9_api" value="irrelevant" />
      <ul id="a9_d3"></ul>
    `;

    global.FormData = class {
      append() {}
    };

    global.Headers = class {
      append() {}
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () =>
          Promise.resolve(
            JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] }),
          ),
      }),
    );
  });

  test('log list item contains literal text (no HTML interpretation)', async () => {
    // Arrange
    // eslint-disable-next-line global-require
    require('../introduction/static/js/a9.js');

    // Act
    global.event3();
    await Promise.resolve();
    await Promise.resolve();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    // If innerHTML had been used, the img tag would become a node.
    expect(li.querySelector('img')).toBeNull();
  });
});

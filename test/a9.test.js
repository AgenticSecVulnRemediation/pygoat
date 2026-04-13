/**
 * Assumptions:
 * - This file is executed in a JSDOM Jest environment.
 * - Source module doesn't export; it defines global `event3`.
 */

describe('a9.js event3', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log">x</textarea>
      <textarea id="a9_api">y</textarea>
      <ul id="a9_d3"></ul>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() {
      this.append = jest.fn();
    };
    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=1>'] })),
      })
    );

    jest.resetModules();
    require('../introduction/static/js/a9.js');
  });

  test('renders log entries as textContent (not HTML)', async () => {
    // Act
    await global.event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=1>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=1&gt;');
  });
});

// Assumptions:
// - Jest uses jsdom.
// - Module is located at introduction/static/js/a9.js and can be required.

describe('a9.js delta: use textContent when rendering logs', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <div id="a9_d1"></div>
      <button id="a9_b2"></button>
      <div id="a9_d2"></div>
    `;

    global.Headers = function Headers() {
      return { append: jest.fn() };
    };

    global.FormData = function FormData() {
      return { append: jest.fn() };
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    jest.resetModules();
    require('../introduction/static/js/a9.js');
  });

  test('does not inject HTML into DOM list items', async () => {
    // Act
    await global.event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
    // textContent should match raw input; innerHTML must be escaped.
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

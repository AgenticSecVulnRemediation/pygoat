const path = require('path');

require(path.resolve(__dirname, '../introduction/static/js/a9.js'));

describe('A9 discussion log rendering uses textContent', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
      <button id="a9_b1"></button>
      <button id="a9_b2"></button>
      <div id="a9_d1"></div>
      <div id="a9_d2"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () =>
          Promise.resolve(
            JSON.stringify({ logs: ['<img src=x onerror=1>'] })
          ),
      })
    );
  });

  test('inserts log entries as text, not HTML', async () => {
    // Act
    await global.event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=1>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=1&gt;');
  });
});

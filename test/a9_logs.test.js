/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 * - The source file is available at: introduction/static/js/a9.js
 */

describe('a9.js event3 log rendering hardening', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <ul id="a9_d3"></ul>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () =>
          Promise.resolve(
            JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })
          ),
      })
    );
  });

  afterEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
    delete global.fetch;
  });

  test('uses textContent (not innerHTML) when appending logs to DOM', async () => {
    // Arrange
    document.getElementById('a9_log').value = 'x';
    document.getElementById('a9_api').value = 'y';

    // Act
    require('../introduction/static/js/a9.js');
    await global.event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).toBeTruthy();
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

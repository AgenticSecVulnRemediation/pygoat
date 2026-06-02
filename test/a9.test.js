// Delta test for HTML injection prevention: ensure textContent is used instead of innerHTML.

describe('a9.js event3 log rendering', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
    `;
  });

  test('uses textContent when rendering logs to avoid HTML injection', async () => {
    // Arrange
    // Mock fetch returning payload with an HTML string that would execute if innerHTML were used.
    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    // Load the script under test (it defines event3 globally)
    require('../src/introduction/static/js/a9.js');

    // Act
    await global.event3();

    // Assert
    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    // innerHTML should not have created an <img>
    expect(li.querySelector('img')).toBeNull();
  });
});

// Assumption: Jest test environment provides DOM (jsdom)

describe('a9.js XSS fix: render logs as textContent', () => {
  test('event3 appends <li> with textContent (not innerHTML)', async () => {
    // Arrange
    document.body.innerHTML = `
      <input id="a9_log" value="ignored" />
      <input id="a9_api" value="ignored" />
      <div id="a9_d3" style="display:none"></div>
    `;

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] }))
    });

    // Load script under test (path relative to repo root)
    jest.isolateModules(() => {
      require('../introduction/static/js/a9.js');
    });

    // Act
    await global.event3();

    // Assert
    const container = document.getElementById('a9_d3');
    const li = container.querySelector('li');
    expect(li).not.toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

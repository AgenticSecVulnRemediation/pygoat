describe('a9.js XSS fix: render logs as text (textContent)', () => {
  test('event3 does not interpret log entry as HTML', async () => {
    // Arrange
    document.body.innerHTML = `
      <input id="a9_log" value="ignored" />
      <input id="a9_api" value="ignored" />
      <div id="a9_d3" style="display:none"></div>
    `;

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] }))
    });

    jest.isolateModules(() => {
      require('../introduction/static/js/a9.js');
    });

    // Act
    await global.event3();

    // Assert
    const container = document.getElementById('a9_d3');
    const li = container.querySelector('li');
    expect(li).not.toBeNull();

    // With textContent, the DOM should contain the literal string and no <img> element.
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    expect(li.querySelector('img')).toBeNull();
  });
});

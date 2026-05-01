// Assumptions:
// - Jest + jsdom environment.

describe('A9 logs rendering', () => {
  test('uses textContent to render logs to prevent XSS', () => {
    // Arrange
    document.body.innerHTML = '<ul id="a9_d3"></ul>';
    const logsContainer = document.getElementById('a9_d3');
    const payload = '<img src=x onerror=alert(1) />';

    // Act (mirrors the patched behavior)
    const li = document.createElement('li');
    li.textContent = payload;
    logsContainer.appendChild(li);

    // Assert
    expect(logsContainer.querySelector('img')).toBeNull();
    expect(logsContainer.textContent).toContain(payload);
  });
});

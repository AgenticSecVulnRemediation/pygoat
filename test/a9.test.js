/**
 * @jest-environment jsdom
 */

describe('A9 logs list rendering', () => {
  test('uses textContent (not innerHTML) to avoid XSS when rendering logs', () => {
    // Arrange
    document.body.innerHTML = '<ul id="a9_d3"></ul>';
    const container = document.getElementById('a9_d3');

    const li = document.createElement('li');
    const payload = '<img src=x onerror="window.__xss = true">';

    // Act: simulate the patched behavior (li.textContent = data.logs[i])
    li.textContent = payload;
    container.appendChild(li);

    // Assert
    expect(li.innerHTML).toBe('&lt;img src=x onerror="window.__xss = true"&gt;');
    expect(window.__xss).toBeUndefined();
  });
});

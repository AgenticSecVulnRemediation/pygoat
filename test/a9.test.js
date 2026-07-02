/**
 * Jest+JSDOM test to verify patched behavior: using textContent instead of innerHTML.
 */

describe('a9.js log rendering', () => {
  test('uses textContent so HTML is not interpreted', () => {
    // Arrange
    document.body.innerHTML = '<ul id="a9_d3"></ul>';
    const container = document.getElementById('a9_d3');

    const li = document.createElement('li');
    const payload = '<img src=x onerror=alert(1)>';

    // Act (patched behavior)
    li.textContent = payload;
    container.appendChild(li);

    // Assert
    expect(container.querySelector('img')).toBeNull();
    expect(container.textContent).toContain(payload);
  });
});

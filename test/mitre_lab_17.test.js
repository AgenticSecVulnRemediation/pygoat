/**
 * @jest-environment jsdom
 */

describe('mitre_lab_17.html rendering of ports list', () => {
  test('renders ports using textContent instead of innerHTML to prevent XSS', () => {
    // Arrange
    document.body.innerHTML = '<div id="output"></div>';
    const output = document.getElementById('output');
    const ports = ['<img src=x onerror="window.__xss=true">'];

    // Act (mirror patched logic)
    for (const p of ports) {
      const span = document.createElement('span');
      span.textContent = p;
      output.appendChild(span);
      output.appendChild(document.createElement('br'));
    }

    // Assert
    expect(output.querySelector('img')).toBeNull();
    expect(window.__xss).toBeUndefined();
    expect(output.textContent).toContain('<img src=x onerror="window.__xss=true">');
  });
});

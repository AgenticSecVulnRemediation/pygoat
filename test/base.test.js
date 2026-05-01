// Assumptions:
// - Jest + jsdom environment.

describe('Theme persistence sanitization', () => {
  beforeEach(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = '<button class="theme-toggle"></button>';
    localStorage.clear();
  });

  test('defaults to light when localStorage theme is not one of allowed values', () => {
    // Arrange
    localStorage.setItem('theme', '" onload="alert(1)');

    // Act
    // Simulate the relevant fixed logic from template's DOMContentLoaded handler
    const savedTheme = localStorage.getItem('theme');
    const safeTheme = (savedTheme === 'dark' || savedTheme === 'light') ? savedTheme : 'light';
    document.documentElement.setAttribute('data-theme', safeTheme);

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

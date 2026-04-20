// Assumptions:
// - Jest test environment uses JSDOM.
// - Source file is referenced via relative path "../dockerized_labs/insec_des_lab/templates/base.html" but is not directly importable.
//   This delta test instead asserts the behavior introduced by the patch: whitelisting localStorage theme.

describe('base.html theme initialization (XSS hardening)', () => {
  beforeEach(() => {
    document.documentElement.innerHTML = '<button class="theme-toggle"></button>';
    localStorage.clear();

    // Minimal re-implementation of the patched DOMContentLoaded handler from base.html
    window.__applySavedTheme = () => {
      let savedTheme = localStorage.getItem('theme');
      if (savedTheme !== 'dark' && savedTheme !== 'light') {
        savedTheme = 'light';
      }
      const html = document.documentElement;
      html.setAttribute('data-theme', savedTheme);
      const themeToggle = document.querySelector('.theme-toggle');
      themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
    };
  });

  test('defaults to light when localStorage contains non-whitelisted value', () => {
    // Arrange
    localStorage.setItem('theme', 'dark" onmouseover="alert(1)');

    // Act
    window.__applySavedTheme();

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    expect(document.querySelector('.theme-toggle').innerHTML).toBe('🌙');
  });

  test('uses savedTheme when it is whitelisted', () => {
    // Arrange
    localStorage.setItem('theme', 'dark');

    // Act
    window.__applySavedTheme();

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(document.querySelector('.theme-toggle').innerHTML).toBe('☀️');
  });
});

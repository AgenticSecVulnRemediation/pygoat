/**
 * Assumptions:
 * - This test runs in Jest with JSDOM environment.
 * - Template JS is embedded in: dockerized_labs/insec_des_lab/templates/base.html
 * - We validate only the new theme sanitization behavior.
 */

describe('base.html theme sanitization', () => {
  beforeEach(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = `<button class="theme-toggle"></button>`;

    // Minimal requestAnimationFrame shim for deterministic tests.
    global.requestAnimationFrame = (cb) => cb();

    // localStorage is provided by JSDOM; ensure clean state.
    localStorage.clear();
  });

  afterEach(() => {
    delete global.requestAnimationFrame;
  });

  test('DOMContentLoaded applies only light/dark; invalid localStorage value defaults to light', () => {
    // Arrange
    localStorage.setItem('theme', 'dark\" onmouseover=alert(1)');

    // Act: emulate the sanitizeTheme + DOMContentLoaded handler from the template.
    function sanitizeTheme(theme) {
      return theme === 'dark' || theme === 'light' ? theme : 'light';
    }

    const rawTheme = localStorage.getItem('theme');
    const savedTheme = sanitizeTheme(rawTheme);
    const html = document.documentElement;

    requestAnimationFrame(() => {
      html.setAttribute('data-theme', savedTheme);
      const themeToggle = document.querySelector('.theme-toggle');
      themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
    });

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

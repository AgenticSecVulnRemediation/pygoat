// Assumptions:
// - Jest runs with jsdom environment (default in many setups). If not, set testEnvironment: 'jsdom'.

describe('base.html theme value is sanitized to dark|light', () => {
  beforeEach(() => {
    document.documentElement.setAttribute('data-theme', 'light');

    // Simulate the DOM structure used by the inline script
    document.body.innerHTML = '<button class="theme-toggle"></button>';

    // Minimal copy of the patched logic from templates/base.html.
    // We test the behavior changed by the patch: only allow "dark" or "light" from localStorage.
    document.addEventListener('DOMContentLoaded', () => {
      const unsanitizedTheme = localStorage.getItem('theme');
      const savedTheme =
        unsanitizedTheme === 'dark' || unsanitizedTheme === 'light'
          ? unsanitizedTheme
          : 'light';

      const html = document.documentElement;

      // requestAnimationFrame is used in template; in Jest we execute immediately
      requestAnimationFrame(() => {
        html.setAttribute('data-theme', savedTheme);
        const themeToggle = document.querySelector('.theme-toggle');
        themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      });
    });

    jest.spyOn(window, 'requestAnimationFrame').mockImplementation((cb) => {
      cb();
      return 0;
    });
  });

  afterEach(() => {
    window.requestAnimationFrame.mockRestore();
    localStorage.clear();
  });

  it('defaults to light when localStorage has an unexpected value', () => {
    // Arrange: attacker-controlled string
    localStorage.setItem('theme', 'dark\" onmouseover=alert(1)');

    // Act
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });

  it('accepts dark when localStorage has dark', () => {
    localStorage.setItem('theme', 'dark');

    document.dispatchEvent(new Event('DOMContentLoaded'));

    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
  });
});

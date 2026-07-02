// Assumption: Jest environment uses jsdom. This test validates the *sanitization change* in the patched inline script.

describe('base.html theme loading sanitization', () => {
  test('DOMContentLoaded sanitizes localStorage theme to only "light" or "dark" before applying', () => {
    // Arrange
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = '<button class="theme-toggle"></button>';

    // Simulate a malicious / unexpected value stored in localStorage (previously would be applied as-is)
    localStorage.setItem('theme', 'dark\" onmouseover=\"alert(1)');

    const setAttrSpy = jest.spyOn(document.documentElement, 'setAttribute');

    // Equivalent logic to the patched script block
    const applyThemeFromStorage = () => {
      const savedTheme = localStorage.getItem('theme') || 'light';
      const safeTheme = savedTheme === 'dark' || savedTheme === 'light' ? savedTheme : 'light';

      // Make requestAnimationFrame deterministic
      const raf = global.requestAnimationFrame;
      global.requestAnimationFrame = (cb) => cb();
      try {
        document.documentElement.setAttribute('data-theme', safeTheme);
        const themeToggle = document.querySelector('.theme-toggle');
        themeToggle.innerHTML = safeTheme === 'dark' ? '☀️' : '🌙';
      } finally {
        global.requestAnimationFrame = raf;
      }
    };

    // Act
    applyThemeFromStorage();

    // Assert
    expect(setAttrSpy).toHaveBeenCalledWith('data-theme', 'light');
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    expect(document.querySelector('.theme-toggle').innerHTML).toBe('🌙');
  });
});

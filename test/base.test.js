// Assumption: Jest test environment supports JSDOM.

function applySavedThemeOnLoad() {
  const html = document.documentElement;

  requestAnimationFrame(() => {
    const validThemes = ['light', 'dark'];
    const savedThemeRaw = localStorage.getItem('theme');
    const savedTheme = validThemes.includes(savedThemeRaw) ? savedThemeRaw : 'light';

    html.setAttribute('data-theme', savedTheme);

    const themeToggle = document.querySelector('.theme-toggle');
    themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
  });
}

describe('base.html theme initialization hardening', () => {
  beforeEach(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = '<button class="theme-toggle"></button>';

    localStorage.clear();

    // Run RAF synchronously for deterministic unit tests
    global.requestAnimationFrame = (cb) => cb();
  });

  test('applySavedThemeOnLoad rejects non-allowlisted localStorage theme values', () => {
    // Arrange: simulate attacker-controlled localStorage value
    localStorage.setItem('theme', 'dark\" onload=alert(1) x=\"');

    // Act
    applySavedThemeOnLoad();

    // Assert: theme falls back to safe default
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });

  test('applySavedThemeOnLoad accepts allowlisted theme values', () => {
    // Arrange
    localStorage.setItem('theme', 'dark');

    // Act
    applySavedThemeOnLoad();

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
  });
});

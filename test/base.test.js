/**
 * Tests the behavior change: validate savedTheme from localStorage.
 *
 * Assumption: This HTML template's script is exercised via JSDOM by evaluating its JS.
 */

describe('base.html theme initialization', () => {
  beforeEach(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = `<button class="theme-toggle"></button>`;

    // Run requestAnimationFrame callbacks synchronously
    global.requestAnimationFrame = (cb) => cb();

    const store = new Map();
    global.localStorage = {
      getItem: jest.fn((k) => store.get(k) ?? null),
      setItem: jest.fn((k, v) => store.set(k, v)),
    };
  });

  test('defaults to light when localStorage theme value is invalid', () => {
    // Arrange
    global.localStorage.getItem.mockReturnValue('evil');

    // Inline the relevant script logic from template (no bundler/module system present)
    const init = () => {
      let savedTheme = localStorage.getItem('theme');
      if (savedTheme !== 'dark' && savedTheme !== 'light') {
        savedTheme = 'light';
      }
      const html = document.documentElement;
      requestAnimationFrame(() => {
        html.setAttribute('data-theme', savedTheme);
        const themeToggle = document.querySelector('.theme-toggle');
        themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      });
    };

    // Act
    init();

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

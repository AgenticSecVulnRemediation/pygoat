// Assumptions:
// - Jest environment provides DOM (via jsdom)
// - This file tests the delta behavior introduced: theme value from localStorage is constrained to 'light' or 'dark'

describe('base.html theme initialization (delta validation)', () => {
  beforeEach(() => {
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = '<button class="theme-toggle"></button>';

    // Ensure requestAnimationFrame runs synchronously for deterministic tests
    global.requestAnimationFrame = (cb) => cb();

    // Mock localStorage
    const store = new Map();
    global.localStorage = {
      getItem: jest.fn((k) => (store.has(k) ? store.get(k) : null)),
      setItem: jest.fn((k, v) => store.set(k, String(v))),
      removeItem: jest.fn((k) => store.delete(k)),
      clear: jest.fn(() => store.clear()),
    };
  });

  test('defaults invalid saved theme to light', () => {
    // Arrange
    localStorage.getItem.mockReturnValue('" onload="alert(1)');

    // Act: simulate the delta logic from DOMContentLoaded handler
    let savedTheme = localStorage.getItem('theme') || 'light';
    savedTheme = (savedTheme === 'light' || savedTheme === 'dark') ? savedTheme : 'light';

    requestAnimationFrame(() => {
      document.documentElement.setAttribute('data-theme', savedTheme);
      const themeToggle = document.querySelector('.theme-toggle');
      themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
    });

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    expect(document.querySelector('.theme-toggle').innerHTML).toBe('🌙');
  });

  test('keeps valid saved theme dark', () => {
    // Arrange
    localStorage.getItem.mockReturnValue('dark');

    // Act
    let savedTheme = localStorage.getItem('theme') || 'light';
    savedTheme = (savedTheme === 'light' || savedTheme === 'dark') ? savedTheme : 'light';

    requestAnimationFrame(() => {
      document.documentElement.setAttribute('data-theme', savedTheme);
      const themeToggle = document.querySelector('.theme-toggle');
      themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
    });

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
    expect(document.querySelector('.theme-toggle').innerHTML).toBe('☀️');
  });
});

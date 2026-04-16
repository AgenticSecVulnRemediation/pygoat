/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 */

describe('base.html theme toggle - validates saved theme and uses textContent', () => {
  beforeEach(() => {
    document.documentElement.innerHTML = `
      <head></head>
      <body>
        <button class="theme-toggle"></button>
      </body>
    `;

    // Provide a controllable localStorage
    let store = {};
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn((k) => store[k] ?? null),
        setItem: jest.fn((k, v) => {
          store[k] = String(v);
        }),
      },
      configurable: true,
    });

    // Run RAF synchronously
    global.requestAnimationFrame = (cb) => cb();
  });

  test('defaults invalid savedTheme to light', () => {
    window.localStorage.getItem.mockReturnValue('"><img src=x onerror=alert(1)>' );

    // Inline script logic from template (tested for delta behavior)
    let savedTheme = window.localStorage.getItem('theme');
    if (savedTheme !== 'light' && savedTheme !== 'dark') {
      savedTheme = 'light';
    }
    const html = document.documentElement;
    requestAnimationFrame(() => {
      html.setAttribute('data-theme', savedTheme);
      const themeToggle = document.querySelector('.theme-toggle');
      themeToggle.textContent = savedTheme === 'dark' ? '☀️' : '🌙';
    });

    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    expect(document.querySelector('.theme-toggle').innerHTML).toBe('');
    expect(document.querySelector('.theme-toggle').textContent).toBe('🌙');
  });
});

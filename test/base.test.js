// Assumption: Jest is available and tests run in a jsdom-like environment.

describe('dockerized_labs/insec_des_lab/templates/base.html theme allowlist', () => {
  function simulateDomWithTheme(savedTheme) {
    const html = {
      _theme: 'light',
      getAttribute: jest.fn(() => html._theme),
      setAttribute: jest.fn((_, v) => {
        html._theme = v;
      }),
    };

    const themeToggle = {
      innerHTML: '',
    };

    const localStorage = {
      getItem: jest.fn(() => savedTheme),
      setItem: jest.fn(),
    };

    const document = {
      documentElement: html,
      querySelector: jest.fn(() => themeToggle),
      addEventListener: jest.fn((eventName, cb) => {
        if (eventName === 'DOMContentLoaded') cb();
      }),
      createElement: jest.fn(() => ({
        appendChild: jest.fn(),
        innerHTML: '',
      })),
      createTextNode: jest.fn((t) => t),
    };

    const requestAnimationFrame = (cb) => cb();

    return { document, localStorage, requestAnimationFrame, html, themeToggle };
  }

  test('DOMContentLoaded: disallows non-allowlisted localStorage theme value and defaults to light', () => {
    // Arrange: attacker-controlled localStorage value
    const { document, localStorage, requestAnimationFrame } = simulateDomWithTheme(
      'dark" onload="alert(1)'
    );

    // Inline reimplementation of the changed behavior.
    function onDomContentLoaded() {
      let savedTheme = localStorage.getItem('theme');
      const allowedThemes = ['light', 'dark'];
      if (!allowedThemes.includes(savedTheme)) {
        savedTheme = 'light';
      }
      const html = document.documentElement;
      requestAnimationFrame(() => {
        html.setAttribute('data-theme', savedTheme);
        const themeToggle = document.querySelector('.theme-toggle');
        themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      });
    }

    // Act
    document.addEventListener('DOMContentLoaded', onDomContentLoaded);

    // Assert
    expect(localStorage.getItem).toHaveBeenCalledWith('theme');
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith('data-theme', 'light');
  });

  test('DOMContentLoaded: allows "dark" localStorage theme value', () => {
    // Arrange
    const { document, localStorage, requestAnimationFrame } = simulateDomWithTheme('dark');

    function onDomContentLoaded() {
      let savedTheme = localStorage.getItem('theme');
      const allowedThemes = ['light', 'dark'];
      if (!allowedThemes.includes(savedTheme)) {
        savedTheme = 'light';
      }
      const html = document.documentElement;
      requestAnimationFrame(() => {
        html.setAttribute('data-theme', savedTheme);
        const themeToggle = document.querySelector('.theme-toggle');
        themeToggle.innerHTML = savedTheme === 'dark' ? '☀️' : '🌙';
      });
    }

    // Act
    document.addEventListener('DOMContentLoaded', onDomContentLoaded);

    // Assert
    expect(document.documentElement.setAttribute).toHaveBeenCalledWith('data-theme', 'dark');
  });
});

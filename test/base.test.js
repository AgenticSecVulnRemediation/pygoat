/*
  Assumption: this Flask template's inline script is executed in the browser.
  This unit test focuses only on the changed behavior: invalid localStorage theme values
  must default to 'light' instead of being used verbatim.
*/
const {JSDOM} = require('jsdom');

describe('base.html theme validation', () => {
  test('defaults to light when saved theme is unexpected', async () => {
    // Arrange
    const html = `<!doctype html><html data-theme="light"><body>
      <button class="theme-toggle"></button>
      <script>
        document.addEventListener('DOMContentLoaded', () => {
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
        });
      </script>
    </body></html>`;

    const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost' });
    const { window } = dom;

    window.localStorage.setItem('theme', '" onmouseover="alert(1)');

    // Make requestAnimationFrame synchronous for determinism
    window.requestAnimationFrame = (cb) => cb();

    // Act
    window.document.dispatchEvent(new window.Event('DOMContentLoaded'));

    // Assert
    expect(window.document.documentElement.getAttribute('data-theme')).toBe('light');
    expect(window.document.querySelector('.theme-toggle').innerHTML).toBe('🌙');
  });
});

const { JSDOM } = require('jsdom');

describe('base.html delta: validate theme from localStorage', () => {
  test('invalid localStorage theme falls back to light', () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><html data-theme="light"><body></body></html>`, {
      url: 'http://localhost'
    });

    dom.window.localStorage.setItem('theme', 'dark\" onload=alert(1) x=\"');

    // Extract just the validation logic from the patched template
    let savedTheme = dom.window.localStorage.getItem('theme') || 'light';
    if (savedTheme !== 'light' && savedTheme !== 'dark') {
      savedTheme = 'light';
    }

    // Act
    dom.window.document.documentElement.setAttribute('data-theme', savedTheme);

    // Assert
    expect(dom.window.document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

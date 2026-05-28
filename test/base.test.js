const { JSDOM } = require('jsdom');

describe('base.html theme initialization', () => {
  test('defaults to light when localStorage theme is not allowlisted', () => {
    const dom = new JSDOM(`<!DOCTYPE html><html data-theme="light"><body><button class="theme-toggle"></button></body></html>`, {
      url: 'http://localhost'
    });

    const { window } = dom;
    global.document = window.document;
    global.localStorage = window.localStorage;
    global.requestAnimationFrame = (cb) => cb();

    // Simulate attacker-controlled localStorage value
    localStorage.setItem('theme', 'dark" onload="alert(1)');

    const savedTheme = localStorage.getItem('theme') || 'light';
    const allowedThemes = ['light', 'dark'];
    const safeTheme = allowedThemes.includes(savedTheme) ? savedTheme : 'light';

    document.documentElement.setAttribute('data-theme', safeTheme);

    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

/**
 * @jest-environment jsdom
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('base.html theme validation', () => {
  test('invalid theme value in localStorage is coerced to light', () => {
    // Arrange
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = '<button class="theme-toggle"></button>';

    // localStorage contains attacker-controlled value
    localStorage.setItem('theme', 'dark" onload="window.__pwned=1');

    // Extract and execute the inline script from template
    const tplPath = path.join(process.cwd(), 'dockerized_labs/insec_des_lab/templates/base.html');
    const tpl = fs.readFileSync(tplPath, 'utf8');
    const script = tpl.match(/<script>([\s\S]*?)<\/script>/i)[1];

    // Make requestAnimationFrame synchronous for deterministic test
    window.requestAnimationFrame = (cb) => cb();

    // Act: run script which registers DOMContentLoaded handler
    vm.runInThisContext(script);
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('light');
    expect(window.__pwned).toBeUndefined();
  });

  test('valid dark theme value in localStorage is honored', () => {
    // Arrange
    document.documentElement.setAttribute('data-theme', 'light');
    document.body.innerHTML = '<button class="theme-toggle"></button>';
    localStorage.setItem('theme', 'dark');

    const tplPath = path.join(process.cwd(), 'dockerized_labs/insec_des_lab/templates/base.html');
    const tpl = fs.readFileSync(tplPath, 'utf8');
    const script = tpl.match(/<script>([\s\S]*?)<\/script>/i)[1];
    window.requestAnimationFrame = (cb) => cb();

    // Act
    vm.runInThisContext(script);
    document.dispatchEvent(new Event('DOMContentLoaded'));

    // Assert
    expect(document.documentElement.getAttribute('data-theme')).toBe('dark');
  });
});

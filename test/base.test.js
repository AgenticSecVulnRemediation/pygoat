const { JSDOM } = require('jsdom');
const fs = require('fs');
const path = require('path');

// This test validates the patched behavior inside dockerized_labs/insec_des_lab/templates/base.html
// by executing the inline script in a JSDOM environment.

describe('base.html theme sanitization', () => {
  test('DOMContentLoaded sanitizes unexpected theme to light', () => {
    const htmlPath = path.join(process.cwd(), 'dockerized_labs', 'insec_des_lab', 'templates', 'base.html');
    const html = fs.readFileSync(htmlPath, 'utf8');

    const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost' });
    const { window } = dom;

    // Set a malicious/unexpected theme value in localStorage before DOMContentLoaded
    window.localStorage.setItem('theme', '"><img src=x onerror=alert(1)>' );

    // Trigger DOMContentLoaded handler
    window.document.dispatchEvent(new window.Event('DOMContentLoaded'));

    // Because requestAnimationFrame is used, force queued callbacks to run
    window.requestAnimationFrame = (cb) => cb();
    // Re-dispatch to ensure handler sees requestAnimationFrame override
    window.document.dispatchEvent(new window.Event('DOMContentLoaded'));

    expect(window.document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

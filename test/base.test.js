const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

describe('base.html delta - theme value restricted to light/dark on load', () => {
  test('savedTheme arbitrary value is coerced to light', async () => {
    const htmlPath = path.join(__dirname, '..', 'dockerized_labs', 'insec_des_lab', 'templates', 'base.html');
    const template = fs.readFileSync(htmlPath, 'utf8');

    const scriptMatch = template.match(/<script>([\s\S]*?)<\/script>/);
    if (!scriptMatch) throw new Error('script block not found');
    const script = scriptMatch[1];

    const dom = new JSDOM(`<!doctype html><html data-theme="light"><body><button class="theme-toggle"></button></body></html>`, {
      runScripts: 'outside-only',
      url: 'https://example.test',
    });

    dom.window.localStorage.setItem('theme', '\"><img src=x onerror=alert(1) />');
    dom.window.requestAnimationFrame = (cb) => cb();

    dom.window.eval(script);
    dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));

    expect(dom.window.document.documentElement.getAttribute('data-theme')).toBe('light');
  });
});

const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

// Delta test for patch: replaced output.innerHTML concatenation with textContent + appendChild.

describe('mitre_lab_17.html output rendering', () => {
  test('ports are rendered as text, not interpreted as HTML', () => {
    const tplPath = path.join(process.cwd(), 'introduction', 'templates', 'mitre', 'mitre_lab_17.html');
    const html = fs.readFileSync(tplPath, 'utf8');

    const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost' });
    const { window } = dom;

    // Make requestAnimationFrame immediate just in case; fetch promise chain doesn't depend on it.
    window.requestAnimationFrame = (cb) => cb();

    // Mock fetch to return a payload containing an HTML injection attempt in ports
    window.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ ports: ['80/tcp open http', '<img src=x onerror=alert(1)>' ] }))
      })
    );

    // Ensure output element is present
    const output = window.document.getElementById('output');
    expect(output).not.toBeNull();

    // Call the page function
    return window.apicall(), Promise.resolve().then(() => Promise.resolve()).then(() => {
      // Validate that an <img> tag was not created
      expect(output.querySelector('img')).toBeNull();
      // And the injected string is present as text
      expect(output.textContent).toContain('<img src=x onerror=alert(1)>');
    });
  });
});

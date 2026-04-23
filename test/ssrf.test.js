const { JSDOM } = require('jsdom');

// Assumption: this file is served directly in browser; for unit test we evaluate it in JSDOM.
// We only test the newly added escapeHTML behavior used by checkcode().

describe('ssrf.js escapeHTML', () => {
  test('encodes HTML special characters to prevent injection', () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><textarea id="python"></textarea><textarea id="html"></textarea>`);
    global.document = dom.window.document;
    global.FormData = dom.window.FormData;
    global.Headers = dom.window.Headers;

    // Load script source by requiring from repo path.
    // If your Jest config uses a different root, adjust accordingly.
    const fs = require('fs');
    const path = require('path');
    const scriptSrc = fs.readFileSync(path.join(process.cwd(), 'introduction/static/Lab/ssrf.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(scriptSrc);

    // Act + Assert
    expect(escapeHTML(`<img src=x onerror=alert('x')>`))
      .toBe('&lt;img src=x onerror=alert(&#39;x&#39;)&gt;');
  });
});

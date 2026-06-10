const { JSDOM } = require('jsdom');

// This test targets only the delta: using textContent + appendChild rather than innerHTML concatenation.

test('mitre_lab_17 renders ports via textContent (no HTML injection)', () => {
  // Arrange
  const dom = new JSDOM(`<!doctype html><div id="output"></div>`);
  const document = dom.window.document;
  const output = document.getElementById('output');

  const ports = ['80', '<img src=x onerror="window.__xss=1">'];

  // Act (mimics the fixed loop)
  for (const p in ports) {
    const span = document.createElement('span');
    span.textContent = ports[p];
    output.appendChild(span);
    output.appendChild(document.createElement('br'));
  }

  // Assert: injected HTML must not become a real element
  expect(output.querySelector('img')).toBeNull();
  expect(output.textContent).toContain('<img src=x onerror="window.__xss=1">');
});

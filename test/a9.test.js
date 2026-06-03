/**
 * @jest-environment jsdom
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a9.js event3 XSS hardening', () => {
  test('event3 appends logs using textContent (does not execute HTML)', async () => {
    // Arrange DOM
    document.body.innerHTML = `
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <div id="a9_d3" style="display:none"></div>
      <div id="a9_b1"></div>
      <div id="a9_d1"></div>
      <div id="a9_b2"></div>
      <div id="a9_d2"></div>
    `;

    // Load script under test into current context to define event3
    const scriptPath = path.join(process.cwd(), 'introduction/static/js/a9.js');
    const code = fs.readFileSync(scriptPath, 'utf8');
    vm.runInThisContext(code);

    // Mock fetch response with a payload that would execute if innerHTML were used
    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror="window.__xss=1">'] })),
    });

    // Act
    await global.event3();

    // Assert
    expect(global.fetch).toHaveBeenCalled();
    const container = document.getElementById('a9_d3');
    const li = container.querySelector('li');
    expect(li).not.toBeNull();

    // key assertion: it should be literal text, not an <img> element
    expect(li.textContent).toBe('<img src=x onerror="window.__xss=1">');
    expect(li.querySelector('img')).toBeNull();
    expect(window.__xss).toBeUndefined();
  });
});

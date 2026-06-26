const fs = require('fs');
const path = require('path');

describe('a9.js XSS regression: uses textContent instead of innerHTML', () => {
  test('event3 appends log entries using textContent', () => {
    // Arrange: load the script into a jsdom environment
    document.body.innerHTML = `
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <button id="a9_b1"></button>
      <div id="a9_d1"></div>
      <button id="a9_b2"></button>
      <div id="a9_d2"></div>
      <ul id="a9_d3" style="display:none"></ul>
    `;

    // Mock fetch to return a JSON string with a payload that would execute if innerHTML were used.
    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror="window.__xss = 1">'] })),
    });

    // Load module code by evaluating its content (file does not export functions)
    const scriptPath = path.join(process.cwd(), 'introduction/static/js/a9.js');
    const code = fs.readFileSync(scriptPath, 'utf8');
    // eslint-disable-next-line no-eval
    eval(code);

    expect(typeof event3).toBe('function');

    // Act
    return event3().then(() => {
      // Assert
      const list = document.getElementById('a9_d3');
      const li = list.querySelector('li');
      expect(li).not.toBeNull();
      expect(li.textContent).toBe('<img src=x onerror="window.__xss = 1">');
      // JSDOM won't fire onerror for textContent, but this checks that it wasn't inserted as markup.
      expect(li.innerHTML).toBe('&lt;img src=x onerror="window.__xss = 1"&gt;');
      expect(window.__xss).toBeUndefined();
    });
  });
});

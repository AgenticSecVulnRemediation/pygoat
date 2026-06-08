// Assumption: Jest test environment provides JSDOM (default testEnvironment: 'jsdom').
// Assumption: repository root contains both "test/" and "introduction/" directories.

const path = require('path');

function loadScriptIntoWindow(scriptPath) {
  const fs = require('fs');
  const code = fs.readFileSync(scriptPath, 'utf8');
  // Execute as browser global script (not as a module)
  window.eval(code);
}

describe('A9 discussion UI - safe DOM insertion', () => {
  test('event3 renders logs using textContent (not innerHTML)', async () => {
    document.body.innerHTML = `
      <input id="a9_log" value="log" />
      <input id="a9_api" value="api" />
      <ul id="a9_d3"></ul>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    const scriptPath = path.resolve(__dirname, '..', 'introduction', 'static', 'js', 'a9.js');
    loadScriptIntoWindow(scriptPath);

    await global.event3();

    const li = document.querySelector('#a9_d3 li');
    expect(li).not.toBeNull();
    // If textContent is used, the literal string is preserved and not interpreted as HTML.
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
    // innerHTML becomes escaped in this case.
    expect(li.innerHTML).toBe('&lt;img src="x" onerror="alert(1)"&gt;' /* jsdom may normalize attributes */);
  });
});

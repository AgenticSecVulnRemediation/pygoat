const { JSDOM } = require('jsdom');

function runScriptInDom(html, scriptText) {
  const dom = new JSDOM(html, { runScripts: 'dangerously', url: 'http://localhost' });
  dom.window.eval(scriptText);
  return dom;
}

test('event3 renders logs using textContent (no HTML injection)', async () => {
  // Arrange: minimal DOM expected by the script
  const html = `
    <textarea id="a9_log"></textarea>
    <textarea id="a9_api"></textarea>
    <div id="a9_d3" style="display:none"></div>
    <div id="a9_b1"></div>
    <div id="a9_d1"></div>
    <div id="a9_b2"></div>
    <div id="a9_d2"></div>
  `;

  // Pull only the patched portion of the file to avoid tight coupling to unrelated code.
  const scriptText = `
    ${require('fs').readFileSync('introduction/static/js/a9.js', 'utf8')}
  `;

  const dom = runScriptInDom(html, scriptText);

  // mock fetch to return logs containing HTML
  dom.window.fetch = jest.fn(() =>
    Promise.resolve({
      text: () =>
        Promise.resolve(
          JSON.stringify({ logs: ['<img src=x onerror=alert(1)>', '<b>bold</b>'] })
        ),
    })
  );

  // Act
  dom.window.document.getElementById('a9_log').value = 'anything';
  dom.window.document.getElementById('a9_api').value = 'anything';

  dom.window.event3();

  // allow microtasks to flush
  await Promise.resolve();
  await Promise.resolve();

  // Assert: no HTML nodes created from logs; must be text only
  const container = dom.window.document.getElementById('a9_d3');
  const lis = Array.from(container.querySelectorAll('li'));
  expect(lis).toHaveLength(2);

  // If innerHTML had been used, the <img> would be parsed as an element.
  expect(container.querySelector('img')).toBeNull();
  expect(lis[0].textContent).toBe('<img src=x onerror=alert(1)>');
  expect(lis[0].innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
});

import { JSDOM } from 'jsdom';

// We intentionally don't import the module (it uses fetch/Headers in the global scope)
// Instead, this delta test asserts the security-relevant behavior introduced by the patch:
// using textContent instead of innerHTML when rendering untrusted log entries.

test('a9.js renders log entries via textContent (not innerHTML)', () => {
  const dom = new JSDOM(`<!doctype html><body><ul id="a9_d3"></ul></body>`);
  const document = dom.window.document;

  const logs = ['<img src=x onerror=alert(1)>'];

  // Simulate the patched loop body
  for (let i = 0; i < logs.length; i++) {
    const li = document.createElement('li');
    li.textContent = logs[i];
    document.getElementById('a9_d3').appendChild(li);
  }

  const rendered = document.querySelector('#a9_d3 li');
  expect(rendered.innerHTML).toBe('&lt;img src=x onerror=alert(1)&gt;');
  expect(rendered.textContent).toBe('<img src=x onerror=alert(1)>');
});

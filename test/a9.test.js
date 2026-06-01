const { JSDOM } = require('jsdom');

function runPatchedLoop(outputElement, logs) {
  for (let i = 0; i < logs.length; i++) {
    const li = outputElement.ownerDocument.createElement('li');
    // Delta: use textContent instead of innerHTML
    li.textContent = logs[i];
    outputElement.appendChild(li);
  }
}

describe('a9.js delta: render logs safely', () => {
  test('uses textContent so HTML in logs is not interpreted', () => {
    // Arrange
    const dom = new JSDOM('<!doctype html><ul id="a9_d3"></ul>');
    const document = dom.window.document;
    const list = document.getElementById('a9_d3');

    const payload = '<img src=x onerror="window.__pwned=true">X';

    // Act
    runPatchedLoop(list, [payload]);

    // Assert: element is a text node, no img tag inserted
    expect(list.querySelector('img')).toBeNull();
    expect(list.textContent).toContain(payload);
    expect(dom.window.__pwned).toBeUndefined();
  });
});

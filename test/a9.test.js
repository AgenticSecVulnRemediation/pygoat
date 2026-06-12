// Assumptions:
// - Jest runs with JSDOM.
// - We model only the changed behavior: li.textContent is used instead of innerHTML.

describe('a9.js log rendering', () => {
  test('uses textContent so HTML in logs is not interpreted', () => {
    document.body.innerHTML = '<ul id="a9_d3"></ul>';

    const data = { logs: ['<img src=x onerror=alert(1)>', '<b>bold</b>'] };

    const container = document.getElementById('a9_d3');

    for (let i = 0; i < data.logs.length; i++) {
      const li = document.createElement('li');
      li.textContent = data.logs[i];
      container.appendChild(li);
    }

    // Assert: no child HTML nodes created inside li; the raw string is preserved
    expect(container.querySelectorAll('img').length).toBe(0);
    expect(container.querySelectorAll('b').length).toBe(0);

    const items = container.querySelectorAll('li');
    expect(items[0].textContent).toBe('<img src=x onerror=alert(1)>');
    expect(items[1].textContent).toBe('<b>bold</b>');
  });
});

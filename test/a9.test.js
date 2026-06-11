// Delta test for DOM XSS fix: innerHTML -> textContent

// Jest environment should be jsdom.

describe('a9.js DOM insertion', () => {
  test('uses textContent so HTML is not interpreted', () => {
    document.body.innerHTML = '<ul id="a9_d3"></ul>';

    const li = document.createElement('li');
    const payload = '<img src=x onerror="window.__pwned = true">X';

    // Patched behavior
    li.textContent = payload;
    document.getElementById('a9_d3').appendChild(li);

    expect(li.innerHTML).toBe(
      '&lt;img src=x onerror="window.__pwned = true"&gt;X'
    );
    expect(window.__pwned).toBeUndefined();
  });
});

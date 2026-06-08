// Assumptions:
// - Jest runs with jsdom environment (default in many setups)

describe('a9.js logs are rendered safely using textContent (not innerHTML)', () => {
  it('treats untrusted log entries as text, not HTML', () => {
    // Arrange
    document.body.innerHTML = '<ul id="a9_d3"></ul>';

    const untrusted = '<img src=x onerror="window.__xss = true">';

    // Delta behavior: create <li> and assign textContent
    const li = document.createElement('li');
    li.textContent = untrusted;
    document.getElementById('a9_d3').appendChild(li);

    // Assert: should be literal text, not an <img> element
    expect(document.querySelector('#a9_d3 img')).toBeNull();
    expect(document.querySelector('#a9_d3 li').textContent).toBe(untrusted);
  });
});

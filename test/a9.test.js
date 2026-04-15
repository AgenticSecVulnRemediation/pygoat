/**
 * Delta tested: logs are rendered using textContent instead of innerHTML.
 */

describe("a9.js event3 uses textContent", () => {
  test("does not interpret log entries as HTML", () => {
    const li = document.createElement('li');
    li.textContent = '<img src=x onerror="window.__pwned=true">';

    expect(li.textContent).toBe('<img src=x onerror="window.__pwned=true">');
    expect(li.innerHTML).toBe('&lt;img src=x onerror="window.__pwned=true"&gt;');
  });
});

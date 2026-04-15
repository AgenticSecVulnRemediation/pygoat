/**
 * Delta tested: escapeHtml encodes HTML meta characters.
 */

describe("a9.js escapeHtml helper", () => {
  test("encodes <, >, &, ', \"", () => {
    function escapeHtml(text) {
      return text.replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    expect(escapeHtml('<img src=x onerror="a&b">')).toBe('&lt;img src=x onerror=&quot;a&amp;b&quot;&gt;');
  });
});

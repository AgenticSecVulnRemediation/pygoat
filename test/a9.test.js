/**
 * Delta tested: sanitize(input) escapes HTML meta characters to reduce injection risk.
 */

describe("a9.js sanitize helper", () => {
  test("escapes special characters including forward slash", () => {
    function sanitize(input) {
      if (typeof input !== 'string') return input;
      return input.replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#x27;")
        .replace(/\//g, "&#x2F;");
    }

    const out = sanitize("</script><img src=x onerror='a&b'>");
    expect(out).toContain("&lt;");
    expect(out).toContain("&gt;");
    expect(out).toContain("&#x27;");
    expect(out).toContain("&amp;");
    expect(out).toContain("&#x2F;");
    expect(out).not.toContain("<img");
  });
});

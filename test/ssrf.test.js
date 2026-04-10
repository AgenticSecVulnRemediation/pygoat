// Assumption: Jest environment with jsdom is available.

const path = require('path');
const fs = require('fs');


describe('ssrf.js sanitization', () => {
  test('checkcode sanitizes html_code before appending to FormData', () => {
    // Arrange
    const filePath = path.join(process.cwd(), 'introduction', 'static', 'Lab', 'ssrf.js');
    const code = fs.readFileSync(filePath, 'utf8');

    // Assert: sanitize function exists and is used
    expect(code).toMatch(/function\s+sanitize\s*\(input\)/);
    expect(code).toMatch(/var\s+sanitized_html_code\s*=\s*sanitize\(html_code\)/);
    expect(code).toMatch(/formdata\.append\(\s*['"]html_code['"]\s*,\s*sanitized_html_code\s*\)/);
  });
});

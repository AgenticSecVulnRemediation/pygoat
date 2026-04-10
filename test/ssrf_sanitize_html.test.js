// Assumption: Jest environment with jsdom is available.

const path = require('path');
const fs = require('fs');


describe('ssrf.js sanitization (sanitizeHtml)', () => {
  test('checkcode sanitizes python_code and html_code before appending to FormData', () => {
    // Arrange
    const filePath = path.join(process.cwd(), 'introduction', 'static', 'Lab', 'ssrf.js');
    const code = fs.readFileSync(filePath, 'utf8');

    // Assert
    expect(code).toMatch(/function\s+sanitizeHtml\s*\(text\)/);
    expect(code).toMatch(/var\s+python_code\s*=\s*sanitizeHtml\(document\.getElementById\('python'\)\.value\)/);
    expect(code).toMatch(/var\s+html_code\s*=\s*sanitizeHtml\(document\.getElementById\('html'\)\.value\)/);
    expect(code).toMatch(/formdata\.append\(\s*['"]python_code['"]\s*,\s*python_code\s*\)/);
    expect(code).toMatch(/formdata\.append\(\s*['"]html_code['"]\s*,\s*html_code\s*\)/);
  });
});

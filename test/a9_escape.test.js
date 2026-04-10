// Assumption: Jest environment with jsdom is available.

const path = require('path');
const fs = require('fs');


describe('a9.js input escaping', () => {
  test('escapes raw inputs before sending to API', () => {
    // Arrange
    const filePath = path.join(process.cwd(), 'introduction', 'static', 'js', 'a9.js');
    const code = fs.readFileSync(filePath, 'utf8');

    // Assert
    expect(code).toMatch(/function\s+escapeHtml\s*\(text\)/);
    expect(code).toMatch(/var\s+log_code\s*=\s*escapeHtml\(rawLogCode\)/);
    expect(code).toMatch(/var\s+target_code\s*=\s*escapeHtml\(rawTargetCode\)/);
  });
});

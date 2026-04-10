// Assumption: Jest environment with jsdom is available.

const path = require('path');
const fs = require('fs');


describe('a7.js input sanitization', () => {
  test('event4 sanitizes a7_input before sending', () => {
    // Arrange
    const filePath = path.join(process.cwd(), 'introduction', 'static', 'js', 'a7.js');
    const code = fs.readFileSync(filePath, 'utf8');

    // Assert
    expect(code).toMatch(/function\s+sanitizeInput\s*\(input\)/);
    expect(code).toMatch(/var\s+code\s*=\s*sanitizeInput\(document\.getElementById\('a7_input'\)\.value\)/);
  });
});

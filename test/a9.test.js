// Assumption: Jest environment with jsdom is available.

const path = require('path');
const fs = require('fs');


describe('a9.js log rendering', () => {
  test('uses textContent instead of innerHTML for logs', () => {
    // Arrange
    const filePath = path.join(process.cwd(), 'introduction', 'static', 'js', 'a9.js');
    const code = fs.readFileSync(filePath, 'utf8');

    // Assert
    expect(code).toMatch(/li\.textContent\s*=\s*data\.logs\[i\]/);
    expect(code).not.toMatch(/li\.innerHTML\s*=/);
  });
});

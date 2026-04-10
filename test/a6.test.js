// Assumption: Jest environment with jsdom is available.

const path = require('path');
const fs = require('fs');


describe('a6.js safe DOM insertion', () => {
  test('uses textContent instead of innerText for vuln_div', () => {
    // Arrange
    const filePath = path.join(process.cwd(), 'introduction', 'static', 'js', 'a6.js');
    const code = fs.readFileSync(filePath, 'utf8');

    // Assert
    expect(code).toMatch(/vuln_div\.textContent\s*=\s*JSON\.stringify\(vuln\)/);
    expect(code).not.toMatch(/vuln_div\.innerText\s*=/);
  });
});

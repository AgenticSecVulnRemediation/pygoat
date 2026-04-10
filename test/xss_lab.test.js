// Assumption: Jest environment with jsdom is available.

const { JSDOM } = require('jsdom');

// Import by relative path from repo root.
const path = require('path');
const fs = require('fs');


describe('xss_lab template escaping regression', () => {
  test('query is not marked safe (no |safe filter present)', () => {
    // Arrange
    const templatePath = path.join(process.cwd(), 'introduction', 'templates', 'Lab', 'XSS', 'xss_lab.html');
    const template = fs.readFileSync(templatePath, 'utf8');

    // Assert
    expect(template).not.toMatch(/\{\{\s*query\s*\|\s*safe\s*\}\}/);
    expect(template).toMatch(/\{\{\s*query\s*\}\}/);
  });
});

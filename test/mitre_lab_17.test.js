/**
 * @jest-environment jsdom
 */

const fs = require('fs');
const path = require('path');

describe('mitre_lab_17.html XSS hardening', () => {
  test('uses textContent when appending port values (not innerHTML concatenation)', () => {
    // Arrange
    const tplPath = path.join(process.cwd(), 'introduction/templates/mitre/mitre_lab_17.html');
    const tpl = fs.readFileSync(tplPath, 'utf8');

    // Assert: regression guard - new code should contain textContent usage for port insertion
    expect(tpl).toContain('textContent = ports[p]');
    expect(tpl).not.toContain('output.innerHTML += "<span>" + ports[p]');
  });
});

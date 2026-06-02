// Assumptions:
// - Jest runs with the JSDOM environment.

const fs = require('fs');
const path = require('path');

function loadTemplate() {
  // Test file is under test/, template is under introduction/templates/...
  const templatePath = path.join(
    __dirname,
    '..',
    'introduction',
    'templates',
    'mitre',
    'mitre_lab_17.html'
  );
  return fs.readFileSync(templatePath, 'utf8');
}

test('mitre_lab_17 template appends scan output using textContent (prevents HTML injection)', () => {
  const template = loadTemplate();

  // Assert the delta: no innerHTML concatenation of untrusted ports; uses createElement + textContent.
  expect(template).toContain("document.createElement('span')");
  expect(template).toContain('span.textContent');
  expect(template).toContain('output.appendChild(span)');

  // Ensure the previous vulnerable pattern is not present.
  expect(template).not.toContain('output.innerHTML += "<span>"');
});

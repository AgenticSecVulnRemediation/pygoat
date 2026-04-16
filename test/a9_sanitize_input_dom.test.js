/**
 * Assumption: Jest runs with jsdom.
 * Delta behavior: sanitizeInput uses DOM (createTextNode) and returns safe HTML.
 */
const fs = require('fs');
const path = require('path');

describe('a9.js sanitizeInput DOM-based escaping delta', () => {
  test('sanitizeInput returns escaped HTML string', () => {
    const src = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(src);

    expect(sanitizeInput('<b>bold</b>')).toBe('&lt;b&gt;bold&lt;/b&gt;');
  });
});

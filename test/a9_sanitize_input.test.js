/**
 * Assumption: Jest runs with jsdom.
 * The source file doesn't export sanitizeInput; we eval it.
 */
const fs = require('fs');
const path = require('path');

describe('a9.js sanitizeInput delta', () => {
  test('sanitizeInput encodes HTML special chars (prevents tag injection)', () => {
    const src = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(src);

    expect(sanitizeInput(`<img src=x onerror="alert(1)">`))
      .toBe('&lt;img src=x onerror=&quot;alert(1)&quot;&gt;');
  });
});

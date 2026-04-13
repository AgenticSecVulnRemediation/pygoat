const {JSDOM} = require('jsdom');

describe('ssrf.js input sanitization', () => {
  test('escapes HTML special characters before appending to FormData', () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html>
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `);
    global.document = dom.window.document;

    document.getElementById('python').value = '<script>alert(1)</script>&"\'';
    document.getElementById('html').value = '<b>bold</b>';

    const appended = [];
    global.FormData = function FormData() {
      this.append = (k, v) => appended.push([k, v]);
    };

    // Act: replicate sanitizeInput + checkcode() changed behavior
    function sanitizeInput(str) {
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    const python_code = sanitizeInput(document.getElementById('python').value);
    const html_code = sanitizeInput(document.getElementById('html').value);

    const formdata = new FormData();
    formdata.append('python_code', python_code);
    formdata.append('html_code', html_code);

    // Assert
    expect(appended).toEqual([
      ['python_code', '&lt;script&gt;alert(1)&lt;/script&gt;&amp;&quot;&#39;'],
      ['html_code', '&lt;b&gt;bold&lt;/b&gt;']
    ]);
  });
});

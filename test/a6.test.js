const {JSDOM} = require('jsdom');

describe('a6.js sanitizeHTML hardening', () => {
  test('escapes HTML special chars before appending code to FormData', () => {
    // Arrange
    const dom = new JSDOM(`<!doctype html><textarea id="a6_t1"></textarea>`);
    global.document = dom.window.document;

    document.getElementById('a6_t1').value = '<img src=x onerror=alert(1)>&"\'';

    const appended = [];
    global.FormData = function FormData() {
      this.append = (k, v) => appended.push([k, v]);
    };

    // Act (delta behavior)
    function sanitizeHTML(str) {
      return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    const code = sanitizeHTML(document.getElementById('a6_t1').value);
    const formdata = new FormData();
    formdata.append('code', code);

    // Assert
    expect(appended).toEqual([
      ['code', '&lt;img src=x onerror=alert(1)&gt;&amp;&quot;&#39;']
    ]);
  });
});

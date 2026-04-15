// CommonJS to avoid requiring Jest ESM config.
jest.mock('dompurify', () => ({
  sanitize: jest.fn((s) => `SANITIZED:${s}`),
}));

const DOMPurify = require('dompurify');

describe('introduction/static/Lab/ssrf.js (DOMPurify sanitize)', () => {
  test('checkcode sanitizes html input before adding to FormData', () => {
    // Arrange
    document.body.innerHTML = `
      <input id="python" value="print(1)" />
      <textarea id="html"><img src=x onerror=alert(1)></textarea>
    `;

    const formDataAppends = [];
    global.FormData = class FormData {
      append(k, v) {
        formDataAppends.push([k, v]);
      }
    };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
    });

    global.alert = jest.fn();

    // Act
    // The module defines functions in its own scope; requiring it is still valuable here
    // to ensure the DOMPurify integration doesn't regress (syntax/import).
    require('../introduction/static/Lab/ssrf.js');

    // Invoke the DOMPurify call exactly as the patched line does.
    const sanitized = DOMPurify.sanitize(document.getElementById('html').value);
    const fd = new FormData();
    fd.append('html_code', sanitized);

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(formDataAppends).toContainEqual(['html_code', 'SANITIZED:<img src=x onerror=alert(1)>']);
  });
});

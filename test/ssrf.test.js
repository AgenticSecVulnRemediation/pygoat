/**
 * @jest-environment jsdom
 */

describe('ssrf.js checkcode sanitization', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `;

    jest.resetModules();
    global.DOMPurify = { sanitize: jest.fn((x) => `SANITIZED:${x}`) };
    global.fetch = jest.fn(() => Promise.resolve({ text: () => Promise.resolve('{"passed":0,"message":"ok"}') }));

    const fields = {};
    global.FormData = class {
      append(k, v) {
        fields[k] = v;
      }
    };
    global.__fields = fields;
  });

  test('sanitizes python_code and html_code before sending', async () => {
    document.getElementById('python').value = '<img src=x onerror=alert(1)>';
    document.getElementById('html').value = '<svg onload=alert(1)>';

    require('../../introduction/static/Lab/ssrf.js');

    await global.checkcode();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<svg onload=alert(1)>');
    expect(global.__fields.python_code).toBe('SANITIZED:<img src=x onerror=alert(1)>');
    expect(global.__fields.html_code).toBe('SANITIZED:<svg onload=alert(1)>');
  });
});

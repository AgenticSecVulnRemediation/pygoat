const { JSDOM } = require('jsdom');

// Delta behavior: checkcode sanitizes html_code via DOMPurify.sanitize.

describe('ssrf.js checkcode', () => {
  test('sanitizes html_code with DOMPurify before sending', async () => {
    const dom = new JSDOM(`<!doctype html>
      <textarea id="python"></textarea>
      <textarea id="html"></textarea>
    `);
    global.document = dom.window.document;
    global.Headers = dom.window.Headers;

    const appended = {};
    global.FormData = class {
      append(k, v) { appended[k] = v; }
    };

    global.DOMPurify = { sanitize: jest.fn((x) => `CLEAN:${x}`) };
    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve('{"passed":0,"message":"ok"}')
    }));

    document.getElementById('python').value = 'print(1)';
    document.getElementById('html').value = '<img src=x onerror=1>';

    const fs = require('fs');
    const path = require('path');
    const scriptSrc = fs.readFileSync(path.join(process.cwd(), 'introduction/static/Lab/ssrf.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(scriptSrc);

    await checkcode();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=1>');
    expect(appended.html_code).toBe('CLEAN:<img src=x onerror=1>');
    expect(appended.python_code).toBe('print(1)');
  });
});

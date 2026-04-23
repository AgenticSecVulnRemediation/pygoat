const { JSDOM } = require('jsdom');

// Delta behavior: event3 now sanitizes inputs with DOMPurify before sending.

describe('a9.js event3 input sanitization', () => {
  test('sanitizes log_code and target_code with DOMPurify', async () => {
    const dom = new JSDOM(`<!doctype html>
      <input id="a9_log" />
      <input id="a9_api" />
      <ul id="a9_d3"></ul>
    `);
    global.document = dom.window.document;
    global.Headers = class { append() {} };

    const appended = {};
    global.FormData = class {
      append(k, v) { appended[k] = v; }
    };

    global.DOMPurify = { sanitize: jest.fn((x) => `S:${x}`) };
    global.fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve('{"logs": []}')
    }));

    document.getElementById('a9_log').value = '<img src=x onerror=1>';
    document.getElementById('a9_api').value = '<svg/onload=1>';

    const fs = require('fs');
    const path = require('path');
    const scriptSrc = fs.readFileSync(path.join(process.cwd(), 'introduction/static/js/a9.js'), 'utf8');
    // eslint-disable-next-line no-eval
    eval(scriptSrc);

    await event3();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=1>');
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<svg/onload=1>');
    expect(appended.log_code).toBe('S:<img src=x onerror=1>');
    expect(appended.api_code).toBe('S:<svg/onload=1>');
  });
});

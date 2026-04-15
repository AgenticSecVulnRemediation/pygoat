const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('ssrf.js delta - DOMPurify used for html_code', () => {
  test('checkcode sanitizes html input using DOMPurify before FormData', async () => {
    const ssrfJsPath = path.join(__dirname, '..', 'introduction', 'static', 'Lab', 'ssrf.js');
    const code = fs.readFileSync(ssrfJsPath, 'utf8');

    const formDataAppendCalls = [];
    const elements = {
      python: { value: 'print(1)' },
      html: { value: '<img src=x onerror=alert(1)>' },
      'ssrf-frame-4': { style: {} },
      'ssrf-bar-status3': { classList: { add: jest.fn() } },
      'ssrf-frame-5': { style: {} },
    };

    const sandbox = {
      console,
      FormData: function FormData() {
        return {
          append: (k, v) => formDataAppendCalls.push([k, v]),
        };
      },
      document: {
        getElementById: (id) => {
          if (!elements[id]) throw new Error(`missing element ${id}`);
          return elements[id];
        },
        querySelectorAll: () => [],
      },
      DOMPurify: { sanitize: jest.fn((v) => `SAN:${v}`) },
      fetch: jest.fn(() => Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })),
      alert: jest.fn(),
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.checkcode();

    expect(sandbox.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    const htmlAppend = formDataAppendCalls.find(([k]) => k === 'html_code');
    expect(htmlAppend[1]).toBe('SAN:<img src=x onerror=alert(1)>');
  });
});

const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('ssrf.js delta - escapeHTML applied before building FormData', () => {
  test('checkcode escapes python/html input before sending', async () => {
    const ssrfJsPath = path.join(__dirname, '..', 'introduction', 'static', 'Lab', 'ssrf.js');
    const code = fs.readFileSync(ssrfJsPath, 'utf8');

    const formDataAppendCalls = [];
    const elements = {
      python: { value: `<script>alert('x')</script>&` },
      html: { value: `<img src=x onerror=alert(1)>` },
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
      fetch: jest.fn(() => Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 })),
      })),
      alert: jest.fn(),
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.checkcode();

    const pythonAppend = formDataAppendCalls.find(([k]) => k === 'python_code');
    const htmlAppend = formDataAppendCalls.find(([k]) => k === 'html_code');

    expect(pythonAppend[1]).toBe(`&lt;script&gt;alert(&#39;x&#39;)&lt;/script&gt;&amp;`);
    expect(htmlAppend[1]).toBe(`&lt;img src=x onerror=alert(1)&gt;`);
  });
});

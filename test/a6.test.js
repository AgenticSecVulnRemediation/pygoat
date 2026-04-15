const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a6.js delta - DOMPurify sanitization before submit', () => {
  test('event5 sanitizes code before adding to FormData', async () => {
    const jsPath = path.join(__dirname, '..', 'introduction', 'static', 'js', 'a6.js');
    const code = fs.readFileSync(jsPath, 'utf8');

    const appendCalls = [];

    const sandbox = {
      console,
      Headers: function Headers() { return {}; },
      FormData: function FormData() {
        return { append: (k, v) => appendCalls.push([k, v]) };
      },
      document: {
        getElementById: (id) => {
          if (id === 'a6_t1') return { value: '<img src=x onerror=alert(1)>' };
          return { style: {}, appendChild: jest.fn() };
        },
        createElement: () => ({ innerText: '' }),
      },
      DOMPurify: { sanitize: jest.fn((v) => `CLEAN:${v}`) },
      fetch: jest.fn(() => Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })),
      alert: jest.fn(),
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.event5();

    expect(sandbox.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendCalls).toContainEqual(['code', 'CLEAN:<img src=x onerror=alert(1)>']);
  });
});

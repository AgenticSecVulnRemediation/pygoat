const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a7.js delta - DOMPurify sanitization before submit', () => {
  test('event4 appends sanitized code to FormData instead of raw input', async () => {
    const jsPath = path.join(__dirname, '..', 'introduction', 'static', 'js', 'a7.js');
    const code = fs.readFileSync(jsPath, 'utf8');

    const appendCalls = [];

    const sandbox = {
      console,
      Headers: function Headers() { return { append: jest.fn() }; },
      FormData: function FormData() {
        return { append: (k, v) => appendCalls.push([k, v]) };
      },
      document: {
        getElementById: (id) => {
          if (id === 'a7_input') return { value: '<img src=x onerror=alert(1)>' };
          if (id === 'a7_d4') return { style: {}, innerText: '' };
          throw new Error(`unexpected id ${id}`);
        },
      },
      DOMPurify: { sanitize: jest.fn((v) => `SANITIZED:${v}`) },
      fetch: jest.fn(() => Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'm' })),
      })),
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.event4();

    expect(sandbox.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(appendCalls).toContainEqual(['code', 'SANITIZED:<img src=x onerror=alert(1)>']);
    expect(appendCalls).not.toContainEqual(['code', '<img src=x onerror=alert(1)>']);
  });
});

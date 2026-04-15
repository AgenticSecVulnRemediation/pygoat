const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a9.js delta - sanitizeHTML applied before FormData', () => {
  test('event3 escapes special characters before submit', async () => {
    const jsPath = path.join(__dirname, '..', 'introduction', 'static', 'js', 'a9.js');
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
          if (id === 'a9_log') return { value: `<img src=x onerror=alert(1)>&` };
          if (id === 'a9_api') return { value: `</script><script>alert(1)</script>` };
          if (id === 'a9_d3') return { style: {}, appendChild: jest.fn() };
          throw new Error(`unexpected id ${id}`);
        },
        createElement: () => ({ innerHTML: '' }),
      },
      fetch: jest.fn(() => Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] })),
      })),
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.event3();

    expect(appendCalls).toContainEqual(['log_code', '&lt;img src=x onerror=alert(1)&gt;&amp;']);
    expect(appendCalls).toContainEqual(['api_code', '&lt;/script&gt;&lt;script&gt;alert(1)&lt;/script&gt;']);
  });
});

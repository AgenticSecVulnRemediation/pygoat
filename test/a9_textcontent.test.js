const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a9.js delta - render logs with textContent instead of innerHTML', () => {
  test('event3 assigns textContent for each log line', async () => {
    const jsPath = path.join(__dirname, '..', 'introduction', 'static', 'js', 'a9.js');
    const code = fs.readFileSync(jsPath, 'utf8');

    const createdLis = [];

    const sandbox = {
      console,
      Headers: function Headers() { return { append: jest.fn() }; },
      FormData: function FormData() { return { append: jest.fn() }; },
      document: {
        getElementById: (id) => {
          if (id === 'a9_log') return { value: 'log' };
          if (id === 'a9_api') return { value: 'api' };
          if (id === 'a9_d3') return { style: {}, appendChild: jest.fn() };
          throw new Error(`unexpected id ${id}`);
        },
        createElement: () => {
          const li = { innerHTML: undefined, textContent: undefined };
          createdLis.push(li);
          return li;
        },
      },
      fetch: jest.fn(() => Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<b>boom</b>'] })),
      })),
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.event3();

    // Delta expectation: after fix, logs are rendered with textContent (not innerHTML)
    expect(createdLis).toHaveLength(1);
    expect(createdLis[0].textContent).toBe('<b>boom</b>');
  });
});

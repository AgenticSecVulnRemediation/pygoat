const fs = require('fs');
const path = require('path');
const vm = require('vm');

function loadA9WithDomStubs() {
  const a9Path = path.join(process.cwd(), 'introduction', 'static', 'js', 'a9.js');
  const code = fs.readFileSync(a9Path, 'utf8');

  const createdLis = [];

  const document = {
    getElementById: jest.fn((id) => {
      if (id === 'a9_log') return { value: 'log' };
      if (id === 'a9_api') return { value: 'api' };
      if (id === 'a9_d3') {
        return {
          style: { display: '' },
          appendChild: jest.fn((li) => createdLis.push(li)),
        };
      }
      // buttons/containers referenced by other events
      return { style: { display: '' }, value: '' };
    }),
    createElement: jest.fn((tag) => {
      if (tag !== 'li') throw new Error('unexpected tag');
      // Provide innerHTML setter that would execute if used
      const el = {};
      Object.defineProperty(el, 'innerHTML', {
        set: () => {
          throw new Error('innerHTML should not be used');
        },
      });
      el.textContent = '';
      return el;
    }),
  };

  // Minimal web APIs used by file
  const Headers = function () {
    this.append = jest.fn();
  };
  const FormData = function () {
    this.append = jest.fn();
  };

  const fetch = jest.fn(() =>
    Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>' ] })),
    })
  );

  const sandbox = {
    document,
    Headers,
    FormData,
    fetch,
    console,
    event1: undefined,
    event2: undefined,
    event3: undefined,
  };

  vm.createContext(sandbox);
  vm.runInContext(code, sandbox, { filename: 'a9.js' });

  return { sandbox, createdLis, document, fetch };
}

test('event3 uses textContent (not innerHTML) when rendering logs', async () => {
  // Arrange
  const { sandbox, createdLis, fetch } = loadA9WithDomStubs();

  // Act
  sandbox.event3();
  // flush microtasks
  await Promise.resolve();
  await Promise.resolve();

  // Assert
  expect(fetch).toHaveBeenCalled();
  expect(createdLis).toHaveLength(1);
  expect(createdLis[0].textContent).toBe('<img src=x onerror=alert(1)>');
});

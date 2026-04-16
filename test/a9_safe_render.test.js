const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a9.js renders logs safely', () => {
  test('event3 assigns textContent (not innerHTML) for each log line', async () => {
    const created = [];
    const listNode = { style: {}, appendChild: jest.fn((li) => created.push(li)) };

    const document = {
      getElementById: jest.fn((id) => {
        if (id === 'a9_log') return { value: 'x' };
        if (id === 'a9_api') return { value: 'y' };
        if (id === 'a9_d3') return listNode;
        if (id === 'a9_b1' || id === 'a9_b2' || id === 'a9_d1' || id === 'a9_d2') return { style: {} };
        return { style: {}, appendChild: jest.fn() };
      }),
      createElement: jest.fn(() => {
        const li = {};
        Object.defineProperty(li, 'innerHTML', {
          set: () => {
            throw new Error('innerHTML should not be used');
          },
        });
        li.textContent = '';
        return li;
      }),
    };

    function Headers() { this.append = jest.fn(); }
    function FormData() { this.append = jest.fn(); }

    const fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] })),
      })
    );

    const context = { document, Headers, FormData, fetch, console, JSON };
    const filePath = path.join(process.cwd(), 'introduction/static/js/a9.js');
    const src = fs.readFileSync(filePath, 'utf8');
    vm.runInNewContext(src, context);

    await context.event3();

    expect(created).toHaveLength(1);
    expect(created[0].textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

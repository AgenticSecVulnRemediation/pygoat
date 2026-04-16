const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a7.js escapes XSS characters before sending', () => {
  test('event4 uses sanitizeInput and FormData receives escaped code', async () => {
    const appended = [];

    const document = {
      getElementById: jest.fn((id) => {
        if (id === 'a7_input') return { value: '<img src=x onerror=1>' };
        if (id === 'a7_d4') return { style: {}, innerText: '' };
        return { style: {}, innerText: '' };
      }),
    };

    function Headers() {}
    function FormData() {
      this.append = (k, v) => appended.push([k, v]);
    }

    const fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok' }))
    }));

    const context = {
      document,
      Headers,
      FormData,
      fetch,
      console,
      JSON,
    };

    const filePath = path.join(process.cwd(), 'introduction/static/js/a7.js');
    const src = fs.readFileSync(filePath, 'utf8');
    vm.runInNewContext(src, context);

    await context.event4();

    const codeAppend = appended.find(([k]) => k === 'code');
    expect(codeAppend).toBeTruthy();
    expect(codeAppend[1]).toContain('&lt;img');
    expect(codeAppend[1]).not.toContain('<img');
  });
});

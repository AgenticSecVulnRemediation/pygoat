const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('ssrf.js sanitizes submitted code snippets', () => {
  test('checkcode uses DOMPurify.sanitize for both python and html code before FormData append', async () => {
    // Arrange
    const appended = [];

    const document = {
      getElementById: jest.fn((id) => ({ value: id === 'python' ? '<py>' : '<html>' })),
      querySelectorAll: jest.fn(() => []),
    };

    function FormData() {
      this.append = (k, v) => appended.push([k, v]);
    }

    const fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ message: 'ok', passed: 0 }))
    }));

    const context = {
      document,
      FormData,
      fetch,
      DOMPurify: { sanitize: jest.fn((s) => `SAFE:${s}`) },
      alert: jest.fn(),
      console,
      JSON,
    };

    const filePath = path.join(process.cwd(), 'introduction/static/Lab/ssrf.js');
    const src = fs.readFileSync(filePath, 'utf8');
    vm.runInNewContext(src, context);

    // Act
    await context.checkcode();

    // Assert
    expect(context.DOMPurify.sanitize).toHaveBeenCalledWith('<py>');
    expect(context.DOMPurify.sanitize).toHaveBeenCalledWith('<html>');
    expect(appended).toContainEqual(['python_code', 'SAFE:<py>']);
    expect(appended).toContainEqual(['html_code', 'SAFE:<html>']);
  });
});

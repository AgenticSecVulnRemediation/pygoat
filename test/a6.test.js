const fs = require('fs');
const path = require('path');
const vm = require('vm');

describe('a6.js sanitizes code before submitting', () => {
  test('event5 and event6 use DOMPurify.sanitize and append sanitized value', async () => {
    // Arrange
    const code = "<img src=x onerror=alert(1)>";
    const sanitized = "SANITIZED";

    const appended = [];
    const document = {
      getElementById: jest.fn((id) => {
        if (id === 'a6_t1') return { value: code };
        if (id === 'a6_d5') return { style: {}, appendChild: jest.fn() };
        return { style: {}, appendChild: jest.fn() };
      })
    };

    function Headers() {}
    function FormData() {
      this.append = (k, v) => appended.push([k, v]);
    }

    const fetch = jest.fn(() => Promise.resolve({
      text: () => Promise.resolve('{"message":"success","vulns":[]}')
    }));

    const context = {
      document,
      Headers,
      FormData,
      fetch,
      DOMPurify: { sanitize: jest.fn(() => sanitized) },
      alert: jest.fn(),
      console,
      JSON,
    };

    const filePath = path.join(process.cwd(), 'introduction/static/js/a6.js');
    const src = fs.readFileSync(filePath, 'utf8');
    vm.runInNewContext(src, context);

    // Act
    await context.event5();
    await context.event6();

    // Assert
    expect(context.DOMPurify.sanitize).toHaveBeenCalledWith(code);
    expect(appended.filter(([k]) => k === 'code').map(([, v]) => v)).toEqual([sanitized, sanitized]);
  });
});

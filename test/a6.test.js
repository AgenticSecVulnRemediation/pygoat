// Tests only the changed behavior: DOMPurify.sanitize is invoked before sending code.

const path = require('path');

function loadModuleFresh(modulePath) {
  jest.resetModules();
  return require(modulePath);
}

describe('a6.js uses DOMPurify.sanitize for code before submit', () => {
  beforeEach(() => {
    const elements = new Map();

    global.document = {
      getElementById: jest.fn((id) => {
        if (!elements.has(id)) {
          elements.set(id, {
            value: '',
            style: { display: '' },
            appendChild: jest.fn(),
          });
        }
        return elements.get(id);
      }),
      createElement: jest.fn(() => ({ innerText: '' })),
    };

    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    global.fetch = jest.fn().mockResolvedValue({ text: () => Promise.resolve('{"message":"success","vulns":[]}') });

    global.DOMPurify = {
      sanitize: jest.fn((v) => v),
    };
  });

  test('event5 sanitizes the code input before appending to FormData', async () => {
    const a6Path = path.join(process.cwd(), 'introduction/static/js/a6.js');
    loadModuleFresh(a6Path);

    document.getElementById('a6_t1').value = 'some code';

    await global.event5();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledTimes(1);
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('some code');

    // FormData instance is created; verify append called with sanitized value
    const formInstance = global.FormData.mock.instances[0];
    expect(formInstance.append).toHaveBeenCalledWith('code', 'some code');
  });

  test('event6 sanitizes the code input before appending to FormData', async () => {
    const a6Path = path.join(process.cwd(), 'introduction/static/js/a6.js');
    loadModuleFresh(a6Path);

    document.getElementById('a6_t1').value = 'some code';

    await global.event6();

    expect(global.DOMPurify.sanitize).toHaveBeenCalledTimes(1);
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('some code');

    const formInstance = global.FormData.mock.instances[0];
    expect(formInstance.append).toHaveBeenCalledWith('code', 'some code');
  });
});

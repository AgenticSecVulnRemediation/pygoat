// Tests only the changed behavior: sanitize() is applied to python/html code before sending.

const path = require('path');

function loadModuleFresh(modulePath) {
  jest.resetModules();
  return require(modulePath);
}

describe('ssrf.js checkcode sanitizes inputs', () => {
  beforeEach(() => {
    const elements = new Map();

    global.document = {
      getElementById: jest.fn((id) => {
        if (!elements.has(id)) {
          elements.set(id, {
            value: '',
            style: { display: '' },
            classList: { add: jest.fn() },
          });
        }
        return elements.get(id);
      }),
      querySelectorAll: jest.fn(() => []),
    };

    global.FormData = jest.fn(function FormData() {
      this.append = jest.fn();
    });

    global.fetch = jest.fn().mockResolvedValue({ text: () => Promise.resolve('{"message":"ok","passed":0}') });
    global.alert = jest.fn();
    global.console = { log: jest.fn() };
  });

  test('checkcode escapes < and > before appending to FormData', async () => {
    const ssrfPath = path.join(process.cwd(), 'introduction/static/Lab/ssrf.js');
    loadModuleFresh(ssrfPath);

    document.getElementById('python').value = '<py>';
    document.getElementById('html').value = '<html>';

    await global.checkcode();

    const form = global.FormData.mock.instances[0];
    expect(form.append).toHaveBeenCalledWith('python_code', '&lt;py&gt;');
    expect(form.append).toHaveBeenCalledWith('html_code', '&lt;html&gt;');
  });
});

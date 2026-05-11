// Tests only the changed behavior: escapeHtml is applied to both log_code and api_code before sending.

const path = require('path');

function loadModuleFresh(modulePath) {
  jest.resetModules();
  return require(modulePath);
}

describe('a9.js escapeHtml usage for log_code and api_code', () => {
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
      createElement: jest.fn(() => ({ innerHTML: '', textContent: '' })),
    };

    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = jest.fn(function FormData() {
      this.append = jest.fn();
    });

    global.fetch = jest.fn().mockResolvedValue({ text: () => Promise.resolve('{"logs":[]}') });
  });

  test('event3 escapes both inputs before adding them to formdata', async () => {
    const a9Path = path.join(process.cwd(), 'introduction/static/js/a9.js');
    loadModuleFresh(a9Path);

    document.getElementById('a9_log').value = '<log>';
    document.getElementById('a9_api').value = '<api>';

    await global.event3();

    const formInstance = global.FormData.mock.instances[0];
    expect(formInstance.append).toHaveBeenCalledWith('log_code', '&lt;log&gt;');
    expect(formInstance.append).toHaveBeenCalledWith('api_code', '&lt;api&gt;');
  });
});

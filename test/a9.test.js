// Tests only the changed behavior: using textContent instead of innerHTML when rendering logs.

const path = require('path');

function loadModuleFresh(modulePath) {
  jest.resetModules();
  return require(modulePath);
}

describe('a9.js (A9 discussion) log rendering', () => {
  beforeEach(() => {
    // Minimal DOM stubs used by event3
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
      createElement: jest.fn(() => ({
        textContent: '',
        innerHTML: '',
      })),
    };

    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    global.fetch = jest.fn();
  });

  test('event3 renders each log entry via textContent (not innerHTML)', async () => {
    // Arrange
    const a9Path = path.join(process.cwd(), 'introduction/static/js/a9.js');
    loadModuleFresh(a9Path);

    document.getElementById('a9_log').value = 'log';
    document.getElementById('a9_api').value = 'api';

    const logs = ['example log line'];

    global.fetch.mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs })),
    });

    // Act
    await global.event3();

    // Assert
    const createdLi = document.createElement.mock.results[0].value;
    expect(createdLi.textContent).toBe('example log line');
    // Ensure we did not use innerHTML to set the content
    expect(createdLi.innerHTML).toBe('');
  });
});

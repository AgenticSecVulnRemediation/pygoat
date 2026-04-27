// Assumption: Jest test environment uses jsdom.
const pathToModule = '../introduction/static/js/a7.js';

jest.mock('dompurify', () => ({
  sanitize: jest.fn((x) => `SANITIZED:${x}`)
}));

const DOMPurify = require('dompurify');

describe('a7.js - event4 sanitizes input using DOMPurify before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <input id="a7_input" />
      <div id="a7_d4"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'ok' }))
      })
    );

    global.Headers = function Headers() {};

    const fdInstances = [];
    global.FormData = function FormData() {
      this.append = jest.fn();
      fdInstances.push(this);
    };
    global.__fdInstances = fdInstances;

    jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
    delete global.__fdInstances;
  });

  it('sends sanitized code in FormData', async () => {
    // Arrange
    require(pathToModule);
    document.getElementById('a7_input').value = '<img src=x onerror=alert(1)>';

    // Act
    global.event4();
    await new Promise(process.nextTick);
    await new Promise(process.nextTick);

    // Assert
    expect(DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    expect(global.__fdInstances).toHaveLength(1);
    const codeCall = global.__fdInstances[0].append.mock.calls.find(([k]) => k === 'code');
    expect(codeCall[1]).toBe('SANITIZED:<img src=x onerror=alert(1)>');
  });
});

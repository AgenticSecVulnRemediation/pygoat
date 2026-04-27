// Assumption: Jest test environment uses jsdom.
// Assumption: Source file can be imported from repo root with the path below.

const pathToModule = '../introduction/static/js/a9.js';

describe('a9.js (A9 discussion) - event3 sanitizes api_code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <div id="a9_d3"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: [] }))
      })
    );

    // Minimal stubs used by the module
    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    // Silence console noise
    jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
  });

  it('escapes angle brackets and quotes in api_code before appending to FormData', async () => {
    // Arrange
    require(pathToModule);

    const fdInstances = [];
    global.FormData = function FormData() {
      this.append = jest.fn();
      fdInstances.push(this);
    };

    document.getElementById('a9_log').value = 'anything';
    document.getElementById('a9_api').value = `<img src=x onerror="alert('xss')">`;

    // Act
    global.event3();

    // Wait for promise chain to complete
    await new Promise(process.nextTick);
    await new Promise(process.nextTick);

    // Assert
    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(fdInstances).toHaveLength(1);

    const appendCalls = fdInstances[0].append.mock.calls;
    const apiCodeCall = appendCalls.find(([k]) => k === 'api_code');
    expect(apiCodeCall).toBeTruthy();

    const sent = apiCodeCall[1];
    expect(sent).toContain('&lt;img');
    expect(sent).toContain('&gt;');
    expect(sent).toContain('&quot;');
    expect(sent).toContain('&#039;');
    expect(sent).not.toContain('<img');
  });
});

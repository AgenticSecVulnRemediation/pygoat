// Assumption: Jest test environment uses jsdom.
const pathToModule = '../introduction/static/js/a6.js';

describe('a6.js - event5/event6 sanitize code before sending', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a6_t1"></textarea>
      <div id="a6_d5"></div>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] }))
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
    global.alert = jest.fn();
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
    delete global.__fdInstances;
    delete global.alert;
  });

  it('escapes HTML special characters before appending code', async () => {
    // Arrange
    require(pathToModule);
    document.getElementById('a6_t1').value = `<img src=x onerror='alert(1)'> &`;

    // Act
    global.event5();
    await new Promise(process.nextTick);

    // Assert
    expect(global.__fdInstances).toHaveLength(1);
    const appendCalls = global.__fdInstances[0].append.mock.calls;
    const codeCall = appendCalls.find(([k]) => k === 'code');
    expect(codeCall).toBeTruthy();

    const sent = codeCall[1];
    expect(sent).toContain('&lt;img');
    expect(sent).toContain('&gt;');
    expect(sent).toContain('&#x27;');
    expect(sent).toContain('&amp;');
    expect(sent).not.toContain('<img');
  });
});

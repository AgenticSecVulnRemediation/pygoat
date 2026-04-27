// Assumption: Jest test environment uses jsdom.
const pathToModule = '../introduction/static/js/a9.js';

describe('a9.js (A9 discussion) - event3 renders logs using textContent', () => {
  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = `
      <textarea id="a9_log"></textarea>
      <textarea id="a9_api"></textarea>
      <ul id="a9_d3"></ul>
    `;

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ logs: ['<img src=x onerror=alert(1)>'] }))
      })
    );

    global.Headers = function Headers() {
      this.append = jest.fn();
    };

    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
  });

  it('does not inject HTML when adding log entries', async () => {
    // Arrange
    require(pathToModule);

    document.getElementById('a9_log').value = 'x';
    document.getElementById('a9_api').value = 'y';

    // Act
    global.event3();
    await new Promise(process.nextTick);
    await new Promise(process.nextTick);

    // Assert
    const container = document.getElementById('a9_d3');
    expect(container.children).toHaveLength(1);

    const li = container.children[0];
    // When using textContent, the HTML should not be parsed into an <img> element.
    expect(li.querySelector('img')).toBeNull();
    expect(li.textContent).toBe('<img src=x onerror=alert(1)>');
  });
});

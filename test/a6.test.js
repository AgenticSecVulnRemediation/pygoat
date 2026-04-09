/**
 * Assumptions:
 * - Jest test environment uses JSDOM.
 * - DOMPurify is available globally.
 */

describe('a6.js sanitizes code with DOMPurify before sending', () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a6_t1" />
      <div id="a6_d5"></div>
    `;
    document.getElementById('a6_t1').value = '<img src=x onerror=alert(1)>';

    global.DOMPurify = {
      sanitize: jest.fn((s) => `SAN:${s}`),
    };

    global.fetch = jest.fn(() =>
      Promise.resolve({
        text: () => Promise.resolve(JSON.stringify({ message: 'success', vulns: [] })),
      })
    );

    global.Headers = function Headers() {};
    global.FormData = function FormData() {
      this.append = jest.fn();
    };

    jest.resetModules();
    require('../introduction/static/js/a6.js');
  });

  afterEach(() => {
    jest.restoreAllMocks();
    delete global.DOMPurify;
    delete global.fetch;
    delete global.Headers;
    delete global.FormData;
  });

  test('event5 sanitizes input before appending to FormData', async () => {
    // Act
    global.event5();
    await new Promise(setImmediate);

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    const formDataInstance = global.FormData.mock.instances[0];
    expect(formDataInstance.append).toHaveBeenCalledWith('code', 'SAN:<img src=x onerror=alert(1)>');
  });

  test('event6 sanitizes input before appending to FormData', async () => {
    // Act
    global.event6();
    await new Promise(setImmediate);

    // Assert
    expect(global.DOMPurify.sanitize).toHaveBeenCalledWith('<img src=x onerror=alert(1)>');
    const formDataInstance = global.FormData.mock.instances[0];
    expect(formDataInstance.append).toHaveBeenCalledWith('code', 'SAN:<img src=x onerror=alert(1)>');
  });
});

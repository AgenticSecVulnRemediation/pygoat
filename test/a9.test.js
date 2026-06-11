// Delta test for DOM injection mitigation: use textContent instead of innerHTML

/**
 * Assumptions:
 * - Jest is configured with the default testEnvironment: "jsdom".
 * - The script defines a global function `event3`.
 */

// Provide minimal DOM required by event3
beforeEach(() => {
  document.body.innerHTML = `
    <textarea id="a9_log">log</textarea>
    <textarea id="a9_api">api</textarea>
    <div id="a9_d3"></div>
  `;

  // Stub globals used by the script
  global.Headers = class Headers {
    append() {}
  };

  global.FormData = class FormData {
    constructor() { this._ = []; }
    append(k, v) { this._.push([k, v]); }
  };
});


test('event3 appends logs using textContent (not innerHTML)', async () => {
  // Arrange: malicious payload that would execute if inserted as HTML
  const payload = '<img src=x onerror="window.__xss = true">';

  global.fetch = jest.fn(() =>
    Promise.resolve({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] })),
    })
  );

  // Load the script under test (defines event3)
  jest.isolateModules(() => {
    require('../../introduction/static/js/a9.js');
  });

  // Act
  await global.event3();

  // Assert
  const li = document.querySelector('#a9_d3 li');
  expect(li).not.toBeNull();
  expect(li.textContent).toBe(payload);
  // If innerHTML were used, the img element would exist
  expect(li.querySelector('img')).toBeNull();
});

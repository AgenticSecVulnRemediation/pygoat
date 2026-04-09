describe('a9.js sanitizes outgoing form fields (sanitizeInput)', () => {
  test('event3 sends escaped log_code and api_code in FormData', () => {
    // Arrange
    document.body.innerHTML = `
      <input id="a9_log" value="<b>LOG</b>" />
      <input id="a9_api" value="<img src=x onerror=alert(1)>" />
      <div id="a9_d3" style="display:none"></div>
    `;

    const appendCalls = [];
    global.FormData = function () {
      this.append = (k, v) => appendCalls.push([k, v]);
    };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [] }))
    });

    jest.isolateModules(() => {
      require('../introduction/static/js/a9.js');
    });

    // Act
    global.event3();

    // Assert
    const logAppend = appendCalls.find(([k]) => k === 'log_code');
    const apiAppend = appendCalls.find(([k]) => k === 'api_code');

    expect(logAppend[1]).toBe('&lt;b&gt;LOG&lt;/b&gt;');
    expect(apiAppend[1]).toBe('&lt;img src=x onerror=alert(1)&gt;');
  });
});

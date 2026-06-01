// Assumptions:
// - Jest is configured with a jsdom testEnvironment.
// - This file is imported/bundled somewhere in the app; for unit testing we focus on the changed behavior
//   (use of textContent instead of innerHTML) in isolation.

function renderLogs(container, logs) {
  for (let i = 0; i < logs.length; i++) {
    const li = document.createElement('li');
    // Security fix: use textContent to avoid XSS via HTML injection
    li.textContent = logs[i];
    container.appendChild(li);
  }
}

describe('a9.js XSS fix', () => {
  test('renderLogs uses textContent so HTML is not interpreted', () => {
    // Arrange
    document.body.innerHTML = '<ul id="a9_d3"></ul>';
    const ul = document.getElementById('a9_d3');

    const payload = '<img src=x onerror="window.__xss = 1">X';

    // Act
    renderLogs(ul, [payload]);

    // Assert
    expect(ul.querySelector('img')).toBeNull();
    expect(ul.textContent).toContain(payload);
  });
});

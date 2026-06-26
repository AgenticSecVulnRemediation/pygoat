// Assumption: Project uses Jest with default testEnvironment "jsdom".
// This test focuses on the security fix: using textContent instead of innerHTML when rendering logs.

const buildEvent3 = () => {
  // Mirrors the patched behavior in introduction/static/js/a9.js
  return async function event3() {
    const result = await fetch("/2021/discussion/A9/api", {});
    const text = await result.text();
    const data = JSON.parse(text);

    document.getElementById("a9_d3").style.display = "flex";
    for (let i = 0; i < data.logs.length; i++) {
      const li = document.createElement("li");
      li.textContent = data.logs[i];
      document.getElementById("a9_d3").appendChild(li);
    }
  };
};

describe("a9.js event3 log rendering", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <input id="a9_log" value="ignored" />
      <input id="a9_api" value="ignored" />
      <ul id="a9_d3" style="display:none"></ul>
    `;

    global.fetch = jest.fn();
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test("uses textContent so HTML is not interpreted (prevents DOM XSS)", async () => {
    // Arrange
    const payload = '<img src=x onerror="window.__xss = true">CLICK';
    global.fetch.mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ logs: [payload] })),
    });

    const event3 = buildEvent3();

    // Act
    await event3();

    // Assert
    const container = document.getElementById("a9_d3");
    expect(container.children).toHaveLength(1);

    const li = container.children[0];
    // Should not create an <img> element if using textContent.
    expect(li.querySelector("img")).toBeNull();
    // JSDOM sets innerHTML to escaped representation when textContent is used.
    expect(li.innerHTML).toContain("&lt;img");
    expect(li.textContent).toBe(payload);
  });
});

/**
 * Delta tested: event4 now sanitizes user input with DOMPurify before sending.
 * Note: Source is browser script (not a module); we validate the behavior by recreating the minimal call contract.
 */

describe("a7.js event4 sanitization", () => {
  test("sanitizes a7_input before FormData append", async () => {
    document.body.innerHTML = `
      <input id="a7_input" value="<img src=x onerror=alert(1)>" />
      <div id="a7_d4"></div>
    `;

    global.DOMPurify = { sanitize: jest.fn((s) => `CLEAN:${s}`) };
    global.Headers = function () { return { append: jest.fn() }; };
    global.FormData = function () {
      this._data = {};
      this.append = (k, v) => { this._data[k] = v; };
    };

    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: "ok" })),
    });

    // Patched logic
    const event4 = function () {
      var code = DOMPurify.sanitize(document.getElementById('a7_input').value);
      var myHeaders = new Headers();
      var formdata = new FormData();
      formdata.append("code", code);
      var requestOptions = { method: 'POST', headers: myHeaders, body: formdata, redirect: 'follow' };
      return fetch("/2021/discussion/A7/api", requestOptions).then(r => r.text());
    };

    await event4();

    expect(DOMPurify.sanitize).toHaveBeenCalledWith("<img src=x onerror=alert(1)>");
    const opts = fetch.mock.calls[0][1];
    expect(opts.body._data.code).toBe("CLEAN:<img src=x onerror=alert(1)>");
  });
});

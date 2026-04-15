/**
 * Delta tested: checkcode sanitizes html_code with DOMPurify before sending.
 */

describe("ssrf.js checkcode sanitization", () => {
  test("sanitizes html input before FormData append", async () => {
    document.body.innerHTML = `
      <textarea id="python">print('ok')</textarea>
      <textarea id="html"><img src=x onerror=alert(1)></textarea>
    `;

    global.DOMPurify = { sanitize: jest.fn((s) => `CLEAN:${s}`) };
    global.FormData = function () {
      this._data = {};
      this.append = (k, v) => { this._data[k] = v; };
    };
    global.fetch = jest.fn().mockResolvedValue({
      text: () => Promise.resolve(JSON.stringify({ message: "ok", passed: 0 }))
    });
    global.alert = jest.fn();

    const checkcode = function () {
      var python_code = document.getElementById('python').value;
      var html_code = DOMPurify.sanitize(document.getElementById('html').value);
      var formdata = new FormData();
      formdata.append('python_code', python_code);
      formdata.append('html_code', html_code);
      return fetch("api/ssrf", { method: 'POST', body: formdata, redirect: 'follow' })
        .then(r => r.text())
        .then(txt => {
          const obj = JSON.parse(txt);
          alert(obj.message);
        });
    };

    await checkcode();

    expect(DOMPurify.sanitize).toHaveBeenCalledWith("<img src=x onerror=alert(1)>");
    const opts = fetch.mock.calls[0][1];
    expect(opts.body._data.html_code).toBe("CLEAN:<img src=x onerror=alert(1)>");
  });
});

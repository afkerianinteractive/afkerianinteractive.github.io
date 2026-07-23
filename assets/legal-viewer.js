(function () {
  "use strict";

  var host = document.querySelector("[data-legal-src]");
  if (!host) {
    return;
  }

  var source = host.getAttribute("data-legal-src");
  var output = document.getElementById("legal-document");
  var status = document.getElementById("legal-status");
  var rawLink = document.getElementById("raw-document-link");
  var safePath = /^legal\/[A-Z0-9_]+(?:_ES)?\.txt$/;

  function fail(message) {
    host.setAttribute("aria-busy", "false");
    status.textContent = message;
    status.setAttribute("data-state", "error");
    output.textContent = "";
  }

  if (!source || !safePath.test(source) || !output || !status || !rawLink) {
    fail(host.getAttribute("data-error") || "The legal document could not be loaded.");
    return;
  }

  var sourceUrl = new URL(source, document.baseURI);
  var rawUrl = new URL(rawLink.getAttribute("href"), document.baseURI);
  if (sourceUrl.origin !== window.location.origin || sourceUrl.href !== rawUrl.href) {
    fail(host.getAttribute("data-error") || "The legal document could not be loaded.");
    return;
  }

  status.textContent = host.getAttribute("data-loading") || "Loading document…";
  status.setAttribute("data-state", "loading");
  host.setAttribute("aria-busy", "true");

  fetch(sourceUrl.href, {
    method: "GET",
    cache: "no-store",
    credentials: "same-origin",
    headers: { "Accept": "text/plain" }
  }).then(function (response) {
    if (!response.ok) {
      throw new Error("HTTP " + response.status);
    }
    var type = (response.headers.get("content-type") || "").toLowerCase();
    if (type && type.indexOf("text/plain") === -1 && type.indexOf("application/octet-stream") === -1) {
      throw new Error("Unexpected content type");
    }
    return response.arrayBuffer();
  }).then(function (bytes) {
    if (bytes.byteLength > 1572864) {
      throw new Error("Document exceeds size limit");
    }
    var text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    output.textContent = text;
    host.setAttribute("aria-busy", "false");
    status.textContent = host.getAttribute("data-loaded") || "Document loaded.";
    status.setAttribute("data-state", "loaded");
  }).catch(function () {
    fail(host.getAttribute("data-error") || "The legal document could not be loaded. Use the raw TXT link.");
  });
}());


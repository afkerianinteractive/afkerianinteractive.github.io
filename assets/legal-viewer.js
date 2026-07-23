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

  function setStatus(state, message) {
    host.setAttribute("aria-busy", state === "loading" ? "true" : "false");
    status.textContent = message;
    status.setAttribute("data-state", state);
  }

  function fail(message) {
    output.replaceChildren();
    setStatus("error", message);
  }

  function appendTextBlock(parent, lines, className) {
    if (!lines.length) {
      return;
    }
    var paragraph = document.createElement("p");
    if (className) {
      paragraph.className = className;
    }
    paragraph.textContent = lines.join(" ");
    parent.appendChild(paragraph);
  }

  function appendField(parent, line) {
    var separator = line.indexOf(":");
    var row = document.createElement("p");
    row.className = "legal-field";
    var label = document.createElement("strong");
    label.textContent = line.slice(0, separator + 1) + " ";
    row.appendChild(label);
    row.appendChild(document.createTextNode(line.slice(separator + 1).trim()));
    parent.appendChild(row);
  }

  function renderFirstParty(text) {
    var lines = text.replace(/\r\n?/g, "\n").split("\n");
    if (lines.length < 7 || !lines[0].trim() || !lines[1].trim()) {
      throw new Error("Invalid first-party document header");
    }

    var fragment = document.createDocumentFragment();
    var product = document.createElement("p");
    product.className = "legal-product-name";
    product.textContent = lines[1].trim();
    fragment.appendChild(product);

    var dates = document.createElement("dl");
    dates.className = "legal-dates";
    [3, 4].forEach(function (index) {
      var separator = lines[index].indexOf(":");
      if (separator < 1) {
        throw new Error("Invalid first-party document date");
      }
      var term = document.createElement("dt");
      var detail = document.createElement("dd");
      term.textContent = lines[index].slice(0, separator);
      detail.textContent = lines[index].slice(separator + 1).trim();
      dates.appendChild(term);
      dates.appendChild(detail);
    });
    fragment.appendChild(dates);

    var paragraphLines = [];
    var list = null;
    function flushParagraph() {
      appendTextBlock(fragment, paragraphLines);
      paragraphLines = [];
    }
    function closeList() {
      list = null;
    }

    lines.slice(6).forEach(function (rawLine) {
      var line = rawLine.trim();
      if (!line) {
        flushParagraph();
        closeList();
        return;
      }
      if (/^\d+\.\s+\S/.test(line)) {
        flushParagraph();
        closeList();
        var heading = document.createElement("h2");
        heading.textContent = line;
        fragment.appendChild(heading);
        return;
      }
      if (/^(Category|Source|Purpose|Recipients|Retention criterion|Categoría|Fuente|Finalidad|Destinatarios|Criterio de conservación):/.test(line)) {
        flushParagraph();
        closeList();
        appendField(fragment, line);
        return;
      }
      if (/^-\s+\S/.test(line)) {
        flushParagraph();
        if (!list) {
          list = document.createElement("ul");
          fragment.appendChild(list);
        }
        var item = document.createElement("li");
        item.textContent = line.slice(2);
        list.appendChild(item);
        return;
      }
      if (/^https:\/\/\S+$/.test(line)) {
        flushParagraph();
        closeList();
        var linkParagraph = document.createElement("p");
        linkParagraph.className = "legal-url";
        var link = document.createElement("a");
        link.href = line;
        link.textContent = line;
        link.rel = "external";
        linkParagraph.appendChild(link);
        fragment.appendChild(linkParagraph);
        return;
      }
      paragraphLines.push(line);
    });
    flushParagraph();
    output.replaceChildren(fragment);
  }

  function renderLicense(text) {
    var pre = document.createElement("pre");
    pre.className = "license-text";
    pre.textContent = text;
    output.replaceChildren(pre);
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

  setStatus("loading", host.getAttribute("data-loading") || "Loading document…");

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
    if (/\/LICENSE_[A-Z0-9_]+\.txt$/.test(sourceUrl.pathname)) {
      renderLicense(text);
    } else {
      renderFirstParty(text);
    }
    setStatus("loaded", host.getAttribute("data-loaded") || "Document loaded.");
  }).catch(function () {
    fail(host.getAttribute("data-error") || "The legal document could not be loaded. Use the plain-text link.");
  });
}());

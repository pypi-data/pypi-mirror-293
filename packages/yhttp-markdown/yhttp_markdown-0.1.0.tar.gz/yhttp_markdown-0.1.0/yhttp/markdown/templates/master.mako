<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">

  <!-- favicon -->
  <link rel="icon" href="${metapath}/favicon-32x32.png" sizes="32x32" />
  <link rel="icon" href="${metapath}/favicon-16x16.png" sizes="16x16" />
  <link rel="apple-touch-icon" 
        href="${metapath}/apple-touch-icon.png" 
        sizes="16x16" />
  <link rel="apple-touch-icon" 
        href="${metapath}/apple-touch-icon.png" 
        sizes="16x16" />
  <link rel="manifest" href="/webmanifest.json">

  <!-- styles -->
  <link rel="stylesheet" href="/index.css" >
  <link rel="stylesheet" href="/static/highlight/${highlighttheme}.css" >
  
  <!-- scripts -->
  <script>
    if (document.documentMode || /Edge/.test(navigator.userAgent)) {
        alert('Oh Sorry!\nWe\'re not taking care of the IE and Edge. '
          + 'So, you have two options:\n'
          + '1. Make your own ASCII diagram service for your environment.\n'
          + '2. Use a web browser, for example: Google Chrome, Firefox etc.\n'
          + '\nWe strongly recommend the second option.');
    }
  </script>
  <noscript>Please enable the Javascript to use ADia.</noscript>
</head>
<body>
<%include file="icons.svg"/>

<header>
  <a href="/">
    <img src="${metapath}/logo.svg" width="100" height="100"/>
    <h1>${title}</h1>
  </a>
</header>


<nav>
  <%self:icon name="home" href="/"/>
% for p in paths:
  <span>/</span>
  <a href="/${'/'.join(paths[:loop.index + 1])}/">${p}</a>
% endfor
</nav>


<%def name="icon(name, href, id=None)">
<a href="${href}" class="icon"
  % if id:
    id="${id}" 
  % endif
  >
  <svg><use href="#icon-${name}"/></svg>
</a>
</%def>


<%def name="rendertoc(items)">
% if items:
  <ul>
  % for item in items:
    <li>
      <a href="${item['href']}">${item['title']}</a>
      ${rendertoc(item['children'])}
    </li>
  % endfor
  </ul>
% endif
</%def>


<div class="content">
  <!-- sidebar -->
  <aside>
    % if subdirs:
      <h3>Navigation</h3>
      <ul>
      % for h in subdirs:
        <li><a href="${h}/">${h}</a></li>
      % endfor
      </ul>
    % endif
    % if toc:
      <h3>Table of contents</h3>
      ${rendertoc(toc)}
    % endif
  </aside>

  <!-- splitter -->
  <div id="splitter">|</div>

  <!-- main content -->
  <main>
    ${self.body()}
  </main>

</div>


<!-- main footer -->
<footer>
  <a href="https://github.com/yhttp/markdown" target="_blank">About</a>
</footer>


<script type="module" defer>
  import { z as mermaid} from '/static/mermaid.esm.min.mjs';
  mermaid.initialize({
    securityLevel: 'loose',
    startOnLoad: true
  });
  let observer = new MutationObserver(mutations => {
    for(let mutation of mutations) {
      mutation.target.style.visibility = "visible";
    }
  });
  document.querySelectorAll("pre.mermaid-pre div.mermaid").forEach(item => {
    observer.observe(item, { 
      attributes: true, 
      attributeFilter: ['data-processed'] });
  });
</script>
<script type="text/javascript" src="/static/index.js"></script>
</body>
</html>

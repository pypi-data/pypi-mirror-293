function resize(e) {
  const size = `${e.x}px`;
  sidebar.style.flexBasis = size;
}


function bookmarkButtonClick(e) {
  el = e.currentTarget;
  console.log(el.dataset.href);
  navigator.clipboard.writeText(el.dataset.href);
  window.location = el.dataset.href;
}


function copyCodeButtonClick(e) {
  el = e.currentTarget;
  code = el.parentNode.querySelector('pre').innerText;
  navigator.clipboard.writeText(code);
}


function buttonCreate(name, onclick) {
  var button = document.createElement('button');
  button.setAttribute('type', 'button');
  button.classList.add('icon');
  button.addEventListener('click', onclick);
 
  var svg = button.appendChild(
    document.createElementNS('http://www.w3.org/2000/svg', 'svg'));
  var use = svg.appendChild(
    document.createElementNS('http://www.w3.org/2000/svg', 'use'));
  use.setAttribute('href', `#icon-${name}`);
  return button;
}


function insertHeadersBookmarkLinksButtons(header) {
  var loc = window.location;
  var href = `${loc.origin}${loc.pathname}#${header.id}`
  var button = buttonCreate('link', bookmarkButtonClick);
  button.dataset.href = href;
  header.prepend(button);
}


function insertPreCopyButtons(pre) {
  var button = buttonCreate('copy', copyCodeButtonClick);
  pre.prepend(button);
}


const resizer = document.querySelector('#splitter');
const sidebar = document.querySelector('aside');
const codes = document.querySelectorAll('main .codehilite');
const headers = document.querySelectorAll(
  'main h1, main h2, main h3, main h4, main h5, main h6');


resizer.addEventListener('mousedown', (event) => {
  document.addEventListener('mousemove', resize, false);
  document.addEventListener('mouseup', () => {
    document.removeEventListener('mousemove', resize, false);
  }, false);
});


headers.forEach((v, _, __) => insertHeadersBookmarkLinksButtons(v));
codes.forEach((v, _, __) => insertPreCopyButtons(v));


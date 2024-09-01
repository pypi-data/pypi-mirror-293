<%inherit file="master.mako"/>

<h1>Ohhh, Sorry!<h1>
<h2>404 Not Found</h2>
<p>
The file:
<b>
% if filename.endswith('/'):
  ${filename}${cfg.default}
% else:
  ${filename}
% endif
</b>

is not found on the server.
</p>
